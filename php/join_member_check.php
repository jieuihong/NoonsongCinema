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

$input_name = $_POST['input_name'];
$input_id = $_POST['input_id'];
$input_pw = $_POST['input_pw'];

$query1 = "select ID from MEMBER";
$stmt1 = sqlsrv_query($conn, $query1);

$ids = array();
while ($row = sqlsrv_fetch_array($stmt1)) {
    array_push($ids, rtrim($row['ID']));
}

if (in_array($input_id, $ids)){
    echo "<script> alert(\"중복된 아이이디입니다. 다시 입력해주세요\"); </script>";
    echo "<script> location.href='join_member.php'; </script>";

} else{
    $query2 = "insert into MEMBER(name, id, pw, level, history)
                values ($input_name, $input_id, $input_pw, 'BRONZE', 0)";
    $stmt = sqlsrv_query($conn, $query2);

    echo "<script> alert(\"회원 가입이 완료되었습니다\"); </script>";
    echo "<script> location.href='login.php'; </script>";



}