<?php
	$to = "oxyderkis@gmail.com";
	$subject = "Vacancy enquiry";
	
	$name = $_POST['name'];
	$telephone = $_POST['telephone'];
	$email = $_POST['email'];
	$msg = nl2br($_POST['msg']);
	
	$headers = "From: " . strip_tags($email) . "\r\n";
	$headers .= "Reply-To: ". strip_tags($email) . "\r\n";
	$headers .= "MIME-Version: 1.0\r\n";
	$headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";
		
	$message = '<html><body style="background-colour: #5E33FF;"><h1>Application</h1>';
	$message .= '<table rules="all" cellpadding="10">';
 	$message .= '<tr><td><strong>Name:</strong></td><td>' . strip_tags($name) . '</td></tr>';
	$message .= '<tr><td><strong>Telephone:</strong></td><td>' . strip_tags($telephone) . '</td></tr>';
	$message .= '<tr><td><strong>Email:</strong></td><td>' . strip_tags($email) . '</td></tr>';
	$message .= '<tr><td><strong>Message:</strong></td><td>' . $msg . '</td></tr>';
	$message .= '</table></body></html>';   

	
	mail("oxyderkis@gmail.com",strip_tags($subject),$message, $headers);

	$respond_message = 'Dear ' . strip_tags($name);
	$respond_message .= '<p>Thank you for interest in a position at Redemption Care Services. We shall review your CV and let you know if we want to take your application further.';
	$respond_message .= '<p>Kind regards,';
	$respond_message .= '<p>Ken Dhluni' . '<br>' . 'Director, Redemption Care Services' . '<br>';
	
	$respond_headers = "From: " . strip_tags($to) . "\r\n";
	$respond_headers .= "Reply-To: ". strip_tags($to) . "\r\n";
	$respond_headers .= "MIME-Version: 1.0\r\n";
	$respond_headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

	mail($email,"Thank you for your Application",$respond_message, $respond_headers);

	include("thankyou2.html");
	
	
?>