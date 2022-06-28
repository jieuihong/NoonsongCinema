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
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>회원가입</title>
</head>
<body>
<form method="post" action="join_member_check.php">
    <h1>회원가입 폼</h1>
    <fieldset>
        <legend>입력사항</legend>
        <table>
            <tr>
                <td>아이디</td>
                <td><input type="text" size="35" name="input_id" placeholder="아이디"></td>
            </tr>
            <tr>
                <td>비밀번호</td>
                <td><input type="password" size="35" name="input_pw" placeholder="비밀번호"></td>
            </tr>
            <tr>
                <td>이름</td>
                <td><input type="text" size="35" name="input_name" placeholder="이름"></td>
            </tr>
        </table>

        <input type="submit" value="가입하기" /><input type="reset" value="다시쓰기" />

    </fieldset>
</form>
</body>
</html>