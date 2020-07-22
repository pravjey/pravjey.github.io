<!DOCTYPE html>

<html>

<head>

<title>Minipedia - created by Pravin Jeyaraj</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>


<body>

<center>

<h1>Welcome to Minipedia</h1>

<% for i in range(3): %>
    <br>
<% end %>


<form action="/summary" method="POST">
<p>
<label>What topic do you want to know about?</label>
<p>
<input type="text" name="keyword">

<% for i in range(3): %>
    <br>
<% end %>

<p><label>Number of sentences required:</label>
<select name="length">
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
<option value="5" selected>5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>
</select>

<p><label>Language:</label>
<select name="lang">
<option value="ar">Arabic</option>
<option value="bn">Bengali</option>
<option value="zh">Chinese</option>
<option value="en" selected>English</option>
<option value="fr">French</option>
<option value="de">German</option>
<option value="hi">Hindi</option>
<option value="la">Latin</option>
<option value="ms">Malay</option>
<option value="ru">Russian</option>
<option value="es">Spanish</option>
<option value="sw">Swahili</option>
<option value="ta">Tamil</option>
</select>

<% for i in range(3): %>
    <br>
<% end %>

<p><input type="submit" value="Submit">
</form>
<% for i in range(3): %>
    <br>
<% end %>

<p>&copy 2020 <a href="http://pravinjeyaraj.wordpress.com">Pravin Jeyaraj</a>

<p>This page is powered by <a href="https://donate.wikimedia.org/">Wikipedia</a>

</body>
</center>



</html>