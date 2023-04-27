// Left Sidebar
const menuItems = document.querySelectorAll('.menu-item')

// remove active class from all menu items
const changeActiveItem = () => {
    menuItems.forEach(item =>{
        item.classList.remove("active")
    })
}


menuItems.forEach(item => {
    
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active')
        if(item.id != 'notifications'){
            // document.querySelector('.notifications-popup').classList.add("d-none")
        }else{
            // document.querySelector('.notifications-popup').classList.remove("d-none")
            document.querySelector('#notifications .notification-count').style.display = 'none'
        }
    })
})
    
