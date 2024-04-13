
<?php		
  $con = mysqli_connect('api.mybespokestaff.com','admin','pass','vistagrade') or die(mysqli_error());
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Recognition</title>
</head>
<body style="text-align: center;">
    <h1>Attendance</h1>
    <img id="video_feed" src="{{ url_for('video_feed') }}">
    <video id="video" autoplay></video>
    <script src="main.js"></script>
    <br>
    <br>
</body>
</html>
