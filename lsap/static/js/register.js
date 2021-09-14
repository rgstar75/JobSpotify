const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const usernamesuccessOutput = document.querySelector(".usernamesuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");

const handleToggleInput=(e)=>{
  if(showPasswordToggle.textContent === 'SHOW'){
    showPasswordToggle.textContent = 'HIDE';
    passwordField.setAttribute("type", "text");
  }else{
    showPasswordToggle.textContent = 'SHOW';
    passwordField.setAttribute("type", "password");
  }
}


showPasswordToggle.addEventListener("click",handleToggleInput);


emailField.addEventListener("keyup", (e) => {
  emailVal = e.target.value;

  emailField.classList.remove('is-invalid');
  emailFeedBackArea.style.display = "none";

  if(emailVal.length > 0){
    fetch("/authentication/validate-email",{
      body: JSON.stringify({email: emailVal }),
      method: "POST",
    })
    .then((res) => res.json())
    .then(data=>{
      console.log("data", data);
      if(data.email_error){
        emailField.classList.add('is-invalid');
        emailFeedBackArea.style.display = "block";
        emailFeedBackArea.innerHTML= `<p>${data.email_error}</p>`
      }
    });
  }
});
usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  usernamesuccessOutput.textContent =`Checking ${usernameVal}`;
  usernameField.classList.remove('is-invalid');
  feedBackArea.style.display = "none";

  if(usernameVal.length > 0){
    fetch("/authentication/validate-username",{
      body: JSON.stringify({username: usernameVal }),
      method: "POST",
    })
    .then((res) => res.json())
    .then(data=>{
      console.log("data", data);
      usernamesuccessOutput.style.display = "none";
      if(data.username_error){
        usernameField.classList.add('is-invalid');
        feedBackArea.style.display = "block";
        feedBackArea.innerHTML= `<p>${data.username_error}</p>`
      }
    });
  }

});