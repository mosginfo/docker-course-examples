<?php

$keys = ['MONGO_HOST', 'MONGO_USERNAME', 'MONGO_PASSWORD', 'MONGO_DATABASE'];
$values = array_map('getenv', $keys);
$config = array_combine($keys, $values);

print_r($config);
