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
//    echo "connected!!!!!!!!!!!!!!!!<br>";
} else {
    echo "Connection could not be established.<br />";
    die(print_r(sqlsrv_errors(), true));
}
//DB연결 끝

session_start();

$user_id = $_POST['user_id'];
$user_pw = $_POST['user_pw'];

$query = "select * from MEMBER where ID='$user_id'";
$stmt = sqlsrv_query($conn, $query);
$row = sqlsrv_fetch_array($stmt);

if ($user_id == rtrim($row['ID']) && $user_pw == rtrim($row['PW'])) {
    $_SESSION['user_id'] = $row['ID'];
    $_SESSION['user_name'] = $row['NAME'];
} else {
        echo "<script> alert(\"잘못된 아이디 또는 비밀번호입니다\"); </script>";
}
echo "<script> location.href='login.php'; </script>";

sqlsrv_free_stmt($stmt);
sqlsrv_close($conn);


