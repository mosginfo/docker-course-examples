<?php

use MongoDB\BSON\UTCDateTime;
use MongoDB\Driver\BulkWrite;
use MongoDB\Driver\Command;
use MongoDB\Driver\Exception\Exception as MongoException;
use MongoDB\Driver\Manager;


function getConfig($varName, $required=false)
{
    if ($secretFile = getenv($varName . '_FILE')) {
        return trim(file_get_contents($secretFile));
    }

    if (($value = getenv($varName)) === false && $required) {
        error_log('Environment variable ' . $varName . ' is required to set.');
        die;
    }

    return $value;
}


function getManager($host, $username, $password)
{
    return new Manager("mongodb://$host", [
        'username' => $username,
        'password' => $password,
        'authSource' => 'admin',
    ]);
}


function logVisit(Manager $manager, $db)
{
    $now = new DateTime('now', new DateTimeZone('UTC'));
    $bulk = new BulkWrite();
    $bulk->insert([
        'ip' => $_SERVER['REMOTE_ADDR'],
        'browser' => $_SERVER['HTTP_USER_AGENT'],
        'timestamp' => new UTCDateTime($now),
    ]);
    return $manager->executeBulkWrite("$db.access_log", $bulk);
}


function queryVisits(Manager $manager, $db)
{
    $pipeline = [
        [
            '$match' => [
                'ip' => $_SERVER['REMOTE_ADDR'],
            ],
        ],
        [
            '$group' => [
                '_id' => '$browser',
                'count' => ['$sum' => 1],
                'lastVisit' => ['$max' => '$timestamp'],
            ],
        ],
        [
            '$project' => [
                '_id' => 0,
                'browser' => '$_id',
                'count' => 1,
                'lastVisit' => 1,
            ],
        ],
    ];
    $command = new Command([
        'aggregate' => 'access_log',
        'pipeline' => $pipeline,
        'cursor' => new stdClass,
    ]);
    return $manager->executeCommand($db, $command)
                   ->toArray();
}


$manager = getManager(
    getConfig('MONGO_HOST'),
    getConfig('MONGO_USERNAME'),
    getConfig('MONGO_PASSWORD'),
);
$db = getConfig('MONGO_DATABASE');

try {
    logVisit($manager, $db);

    $response = [];

    foreach (queryVisits($manager, $db) as $row) {
        $row->lastVisit = $row->lastVisit->toDateTime()->format('c');
        $response[] = $row;
    }
} catch(MongoException $err) {
    error_log($err->getMessage());
    http_response_code(500);
    $response = [
        'error' => [
            'code' => 500,
            'message' => 'Internal Server Error'
        ]
    ];
}


header('Content-Type: application/json');
echo json_encode($response, JSON_UNESCAPED_SLASHES) . "\n";
