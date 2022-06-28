<HTML>
<head>
    <title>noonsong cinema</title>
    <meta charset="utf-8">
</head>

<body>
    <center>
    <table border="3">
        <tr>
            <td><a href="now_showing.php"> 현재 상영중인 영화 </a></td>
            <td><a href="buy_ticket.php"> 영화 예매 </a></td>
            <td><a href="my_page.php"> 마이 페이지 </a></td>
        </tr>
    </table>
    </center>
</body>

<?php

error_reporting(E_ALL);
ini_set("display_errors", 1);

echo "hello <br>";

$server = 'localhost, 51850';
$database = 'Cinema2';

$conn_info = array(
    "Database" => $database,
    "CharacterSet" => "UTF-8"
);

$conn = sqlsrv_connect($server, $conn_info);

if ($conn) {
    echo "connected!!!!!!!!!!!!!!!!<br>";
} else {
    echo "Connection could not be established.<br />";
    die(print_r(sqlsrv_errors(), true));
}

$query = 'select * from MEMBER';

$stmt = sqlsrv_query($conn, $query);

while ($row = sqlsrv_fetch_array($stmt)) {
    echo rtrim($row['NAME']);
    echo rtrim($row['ID']);
    echo rtrim($row['PW']);
    echo rtrim($row['LEVEL']);
    echo "<br>\n";
}

sqlsrv_free_stmt($stmt);
sqlsrv_close($conn);

echo "<script> alert(\"로그인에 성공하였습니다\"); </script>"

?>
</HTML>


