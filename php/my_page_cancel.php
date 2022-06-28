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

<h2>마이페이지</h2>
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
session_start();


$user_id = $_SESSION['user_id'];
$user_name = $_SESSION['user_name'];

$query = "select LEVEL from MEMBER where ID='$user_id'";
$stmt = sqlsrv_query($conn, $query);
$row = sqlsrv_fetch_array($stmt);

$user_level = $row['LEVEL'];

echo "$user_name($user_id)님의 등급은 $user_level 입니다";
echo "&nbsp;<a href='logout.php'><input type='button' value='Logout'></a> <br><br>";

//여기까지 마이페이지 기본 틀

$booked = $_SESSION['booked'];
$canceled = $_POST['cancel_movie'];

if(in_array($canceled, $booked)){
    $query = "delete from RESERVATION where memberID=$user_id and movieID=$canceled";
    $stmt = sqlsrv_prepare($conn, $query);
    if (!$stmt){
        die(print_r(sqlsrv_errors(), true));
    }

    if (!sqlsrv_execute($stmt)){
        die(print_r(sqlsrv_errors(), true));
    } else {
        echo "<script> alert(\"취소가 완료되었습니다\"); </script>";
        echo "<script> location.href='my_page_booked.php'; </script>";
    }

    sqlsrv_rows_affected($stmt);
} else {
    echo "<script> alert(\"예매 내역에 없는 영화입니다. 다시 입력해주세요\"); </script>";
    echo "<script> location.href='my_page_booked.php'; </script>";
}
?>

</body>
</HTML>