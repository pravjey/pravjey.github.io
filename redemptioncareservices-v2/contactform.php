<?php
	$to = "oxyderkis@gmail.com";
	
	$subject = $_POST['enquiry'];
	$name = $_POST['name'];
	$jobtitle = $_POST['jobtitle'];
	$org = $_POST['org'];
	$telephone = $_POST['telephone'];
	$email = $_POST['email'];
	$msg = $_POST['msg'];
	
	$headers = "From: " . strip_tags($email) . "\r\n";
	$headers .= "Reply-To: ". strip_tags($email) . "\r\n";
	$headers .= "MIME-Version: 1.0\r\n";
	$headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";
		
	$message = '<html><body style="background-colour: #5E33FF;"><h1>Submitted information</h1>';
	$message .= '<table rules="all" cellpadding="10">';
 	$message .= '<tr><td><strong>Name:</strong></td><td>' . strip_tags($name) . '</td></tr>';
	$message .= '<tr><td><strong>Job Title:</strong></td><td>' . strip_tags($jobtitle) . '</td></tr>';
	$message .= '<tr><td><strong>Organisation:</strong></td><td>' . strip_tags($org) . '</td></tr>';
	$message .= '<tr><td><strong>Telephone:</strong></td><td>' . strip_tags($telephone) . '</td></tr>';
	$message .= '<tr><td><strong>Email:</strong></td><td>' . strip_tags($email) . '</td></tr>';
	$message .= '<tr><td><strong>Message:</strong></td><td>' . strip_tags($msg) . '</td></tr>';
	$message .= '</table></body></html>';
	
	mail("oxyderkis@gmail.com",strip_tags($subject),$message, $headers);

	$respond_message = 'Dear ' . strip_tags($name);
	$respond_message .= '<p>Thank you for contacting Redemption Care Services. We shall endeavour to get in touch as quickly as possible.';
	$respond_message .= '<p>Kind regards,';
	$respond_message .= '<p>Ken Dhluni' . '<br>' . 'Director, Redemption Care Services' . '<br>';
	
	$respond_headers = "From: " . strip_tags($to) . "\r\n";
	$respond_headers .= "Reply-To: ". strip_tags($to) . "\r\n";
	$respond_headers .= "MIME-Version: 1.0\r\n";
	$respond_headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

	mail($email,"Thank you for your Enquiry",$respond_message, $respond_headers);

	include("thankyou.html");
	
	
?>

