<?php
$target_dir = "../ratemypet/static/uploads/";
$target_file = $target_dir . basename($_FILES["photoupload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["photoupload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["photoupload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>