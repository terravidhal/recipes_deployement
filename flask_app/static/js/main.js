window.onload = () =>{
    const icons = document.querySelectorAll('i.icon-password')
    const toggleInputType = (ev) =>{
        ev.target.classList.toggle('fa-eye-slash');
        const input = ev.target.parentNode.children[1];
        //console.log(input);
        input.type === "password" ? input.type = "text" : input.type = "password";
    }
    const setupListeners = () =>{
       for (let index = 0; index < icons.length; index++) {
           const icon = icons[index];
           icon.onclick = toggleInputType
       }
    }
    setupListeners();
}