<HTML>
<head>
    <title>noonsong cinema</title>
    <meta charset="utf-8">
</head>

<body>
    <header><h1>NOONSONG CINEMA 눈송 시네마</h1></header>

        <table border="3">
            <tr>
                <td><a href="now_showing.php"> 현재 상영중인 영화 </a></td>
                <td><a href="buy_ticket.php"> 영화 예매 </a></td>
                <td><a href="my_page.php"> 마이 페이지 </a></td>
            </tr>
        </table>

    <h2>현재 상영 중인 영화</h2>
</body>

<?php

error_reporting(E_ALL);
ini_set("display_errors", 1);

$server = 'localhost, 51850';
$database = 'Noonsong_Cinema';

$conn_info = array(
    "Database" => $database,
    "CharacterSet" => "UTF-8"
);

$conn = sqlsrv_connect($server, $conn_info);

if ($conn) {
    echo "";
} else {
    echo "Connection could not be established.<br />";
    die(print_r(sqlsrv_errors(), true));
}

$query = 'select * from MOVIE';
$stmt = sqlsrv_query($conn, $query);

while ($row = sqlsrv_fetch_array($stmt)) {
    echo rtrim($row['TITLE']), " (", rtrim($row['RUNTIME']), ") | ";
    echo rtrim($row['GENRE']), " | ";
    echo "개봉일: ", rtrim($row['RELEASE']), " | ";
    echo "평점: ", rtrim($row['RATING']), " | ";
    echo "감독: ", rtrim($row['DIRECTOR']);
    echo "<br><br>";
}
sqlsrv_free_stmt($stmt);
sqlsrv_close($conn);
?>
</html>