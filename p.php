<html>
<body>

<?php

if(isset($_POST['submit_button'])) 
{ 
    $site = $_POST['site'];
    $keywords = $_POST['keywords'];

    $output = exec("python page.py $site $keywords");
    #echo "<h1>Output from python: $output</h1>";
    echo "<h1>Site rank by keywords </h1>";
    $s = preg_split('/\s+/', $output);  // spacing as a delimiter
    $rank = $s[1];  
    $url_found = $s[0];  

    echo "Site name : $site <br>";
    echo "Key Words : $keywords<br>";
    echo "<h2>url   : <font color='green'><b>$url_found</b></font><br></h2>";
    if($rank != -1) 
        echo "<h2>Ranking   : <font color='red'><b>$rank</b></font><br></h2>";
    else   
        echo "<h2>Ranking   : <font color='red'><b>not within 100th</b></font><br></h2>";
}
?>

<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
<table border="0">
 <tr>
  <td width="200">Site Name (example.com)</td>
  <td width="300"> 
    <input type="text" value="<?php if($site) {echo $site; } ?>" 
                        name="site" size="50" maxlength="300"/>
  </td>
 </tr>
 <tr>
  <td width="200">Key Words (kew1 key2 ...)</td>
  <td width="300"> 
    <input type="text" value="<?php if($keywords) {echo $keywords; } ?>" 
                        name="keywords" size="50" maxlength="500"/>
  </td>
</tr>
<tr>
 <td></td> 
</tr>
<tr>
 <td>
<input type="submit" name="submit_button" value="Get site rank by keywords" 
 style="background:mediumseagreen; color:#ffffff; font-weight:bold;
 width:200px; height:30px"/>
 </td>
 <td></td> <td></td> <td></td> <td></td>
</tr>
</table>
</form>
 
<?php
$site = $_POST['site'];
$keywords = $_POST['keywords'];
?>

</html>
