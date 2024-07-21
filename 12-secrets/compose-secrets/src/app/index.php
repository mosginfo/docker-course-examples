<?php
declare(strict_types=1);

use MongoDB\BSON\UTCDateTime;
use MongoDB\Driver\BulkWrite;
use MongoDB\Driver\Command;
use MongoDB\Driver\Exception\Exception as MongoException;
use MongoDB\Driver\Manager;


function getConfig(string $varName, bool $required=false): string
{
    if ($secretFile = getenv($varName . '_FILE')) {
        return trim(file_get_contents($secretFile));
    }

    if (($value = getenv($varName)) === false && $required) {
        throw new Exception('Environment variable ' . $varName . ' is required to set.');
    }

    return $value;
}


function getManager(string $host, string $username, string $password): Manager
{
    return new Manager("mongodb://$host", [
        'username' => $username,
        'password' => $password,
        'authSource' => 'admin',
    ]);
}


function logVisit(Manager $manager, string $db)
{
    $now = new DateTime('now', new DateTimeZone('UTC'));
    $bulk = new BulkWrite();
    $bulk->insert([
        'ip' => $_SERVER['REMOTE_ADDR'],
        'browser' => $_SERVER['HTTP_USER_AGENT'],
        'timestamp' => new UTCDateTime($now),
    ]);
    $manager->executeBulkWrite("$db.access_log", $bulk);
}


function queryVisits(Manager $manager, string $db): array
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


try {
    $manager = getManager(
        getConfig('MONGO_HOST', true),
        getConfig('MONGO_USERNAME', true),
        getConfig('MONGO_PASSWORD', true),
    );
    $db = getConfig('MONGO_DATABASE', true);

    logVisit($manager, $db);

    $response = [];

    foreach (queryVisits($manager, $db) as $row) {
        $row->lastVisit = $row->lastVisit->toDateTime()->format('c');
        $response[] = $row;
    }
} catch(Exception $err) {
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
