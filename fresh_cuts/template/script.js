function valid(){
    document.getElementById("num_error").innerHTML=""
    document.getElementById("pin_error").innerHTML=""
    document.getElementById("email_error").innerHTML=""

    name=document.getElementById("name").value
    phno=document.getElementById("phonenumber").value
    email=document.getElementById("Email").value
    location=document.getElementById("location").value
    password=document.getElementById("password").value
    console.log(name,phonenumber,Email,location,password);
    if(phno.length!=10){
        document.getElementById("num_error").innerHTML="invalid number"
    }
    else{
        if(! phno.match('[6-9].{9}')){
            document.getElementById("num_error").innerHTML="invalid number"
        
    }
}
    // if(pin.length!=6){
    //     document.getElementById("pin_error").innerHTML="invalid pin"
    // }
    if(email.match("@gmail.com")){
    }
    else{
        document.getElementById("email_error").innerHTML="invalid email"
    }

}