
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Recognition</title>
</head>
<body style="text-align: center;">
    <h1>Attendance</h1>
    <br>


    <form method="GET" action="/video_feed">

    
        <select name="teacher" style="    background-color: #03A9F4;
    color: white;
    height: 70px;
    width: 320px;
    font-size: 23px;">
    <option value="">Select Teacher</option>
                {% for row in teachers %}
                <option value="{{ row[0] }}">{{ row[1] }} {{ row[2] }}</option>
                {% endfor %}
        </select>

        <br>
    <br>
        <select name="subject" style="    background-color: #03A9F4;
    color: white;
    height: 70px;
    width: 320px;
    font-size: 23px;">
    <option value="">Select Subject</option>    
                {% for row in subjects %}
                <option value="{{ row[0] }}">{{ row[1] }}</option>
                {% endfor %}
        </select>
        <br>
    <br>
        <select name="timeinout" style="    background-color: #03A9F4;
    color: white;
    height: 70px;
    width: 320px;
    font-size: 23px;">
            <option value="">Select</option>
            <option value="Timein">Timein</option>
            <option value="Timeout">Timeout</option>
        </select>
        <br><br>
<button type="submit" style="    background-color: #03A9F4;
    color: white;
    height: 70px;
    width: 320px;
    font-size: 23px;">Submit</button>
</form>
</body>
</html>
