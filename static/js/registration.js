function showRegistration(){
    document.querySelector("#regItem").style.display = "flex";
    document.querySelector("body").classList.add("no-sctoll");
}
function hideRegistration(){
    document.querySelector("body").classList.remove("no-sctoll");
    document.querySelector("#regItem").style.display = "none";
    document.getElementsByName("nameInput")[0].value = "";
    document.getElementsByName("tgInput")[0].value = "";
    document.querySelector("#error-message").innerText = "1";
    document.querySelector("#error-message").classList.remove("show-error");
    document.querySelector("#error-message").classList.remove("show-message");
    document.querySelector("#error-message").classList.add("hide-error");
    document.querySelector("#icon").classList.remove("rotate");
    document.querySelector("#icon").innerText = "";
}
function buttonClick(){
    event.preventDefault();
    if(!document.querySelector("#icon").classList.contains("spin")){
        if(checkFill()){
            document.querySelector("#error-message").innerText = "1";
            document.querySelector("#error-message").classList.remove("show-error");
            document.querySelector("#error-message").classList.remove("show-message");
            document.querySelector("#error-message").classList.add("hide-error");
            StartAnimation();
            CheckIsExsistTG();
        }
        else{
            document.querySelector("#error-message").innerText = "Заполните форму";
            document.querySelector("#error-message").classList.add("show-error");
            document.querySelector("#error-message").classList.remove("hide-error");
        }
    }
}

function checkFill(){
    const name = document.getElementsByName("nameInput")[0].value;
    const tgname = document.getElementsByName("tgInput")[0].value;
    return name!="" && tgname!="";
}
function StopAnimation(isOk){
    icon = document.getElementById("icon");
    icon.classList.remove("rotate");
    if(isOk)
        icon.innerText = "check";
    else
        icon.innerText = "close";
        
}
function StartAnimation(){
    icon = document.getElementById("icon");
    icon.innerText = "autorenew"
    icon.classList.add("rotate");
}
function ShowIsOk(isExist){
    if(!isExist){
        document.querySelector("#error-message").innerText = "Телеграм аккаунт не существует или закрыт";
        document.querySelector("#error-message").classList.add("show-error");
        document.querySelector("#error-message").classList.remove("hide-error");
        StopAnimation(false);
    }
}
function ShowIsRegistered(isRegistered){
    if(!isRegistered){
        document.querySelector("#error-message").innerText = "Телеграм аккаунт уже зарегестрирован в турнире";
        document.querySelector("#error-message").classList.add("show-error");
        document.querySelector("#error-message").classList.remove("hide-error");
        StopAnimation(false);
    }
}
async function sendData() {
const name = document.getElementsByName("nameInput")[0].value;
const mmr = document.getElementsByName("mmrInput")[0].value;
const tgname = document.getElementsByName("tgInput")[0].value;
try {
    const dataToSend = {
        'name': name,
        'mmr': mmr,
        'tgname': tgname,
    };
    const response = await fetch('https://tournametsite.onrender.com/send_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },  
        body: JSON.stringify(dataToSend)
    });
    const data = await response.json();  // Получаем данные из ответа
    if (!data["executed"]){
        document.querySelector("#error-message").innerText = "Ошибка при добавлении в базу данных";
        document.querySelector("#error-message").classList.add("show-error");
        document.querySelector("#error-message").classList.remove("hide-error");
        StopAnimation(false);
    }
    else{
        document.querySelector("#error-message").innerText = "Участник успешно добавлен!";
        document.querySelector("#error-message").classList.add("show-message");
        document.querySelector("#error-message").classList.remove("hide-error");
        StopAnimation(true);
    }
}
catch (error) {
    console.error('Ошибка:', error);
}
}
async function CheckIsExsistTG(){
    const name = document.getElementsByName("tgInput")[0].value;
    const dataToSend = {
        name: name
    };
    try {
        const response = await fetch('https://tournametsite.onrender.com/check_tg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },  
            body: JSON.stringify(dataToSend)
        });
        const data = await response.json();
        ShowIsOk(data["acc_exist"]);
        if(data["acc_exist"]){
            const isUnicue = await CheckIsUnicueTg(name); // Ждем асинхронного результата
            ShowIsRegistered(isUnicue);
            if(isUnicue)
                sendData();
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function CheckIsUnicueTg(name){
    const dataToSend = {
        name: name
    };
    try {
        const response = await fetch('https://tournametsite.onrender.com/check_tg_in_db', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },  
            body: JSON.stringify(dataToSend)
        });
        const data = await response.json();
        return data["acc_alright"];
    } catch (error) {
        console.error('Ошибка:', error);
        return false; // Если ошибка, возвращаем false
    }
}
document.querySelector(".button").addEventListener('touchstart', function(event) {
        event.target.classList.add('touch');
});
document.querySelector(".button").addEventListener('touchend', function(event) {
        event.target.classList.remove('touch');
});
