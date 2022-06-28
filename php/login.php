<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Noonsong Cinema</title>
</head>

<body>
<header><h1> NOONSONG CINEMA 눈송 시네마</h1></header>


<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

session_start();
if(isset($_SESSION['user_id'])==null){
?>

<!--로그인 창-->
<form action="login_sql.php" method="POST">
    <h2> 로그인 </h2>
        <h4> ID &nbsp: <input type="text" name="user_id" size="15"></h4>
        <h4>PW : <input type="password" name="user_pw" size="15"></h4>
    <input type="submit" value="LOGIN">
    <input type="reset" value="CANCEL">
    <a href="join_member.php"> 회원가입 </a>
</form>

<?php
    } else {
//        echo "로그인에 성공하였습니다";
        echo "<script> alert(\"로그인에 성공하였습니다\"); </script>";
        echo "<script> location.href='my_page.php'; </script>";
    }
?>

</body>
</html>