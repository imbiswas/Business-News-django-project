let boxes = Array.from(document.getElementsByClassName('boxlink'));
function selectBox(id) {
    boxes.forEach(b => {
        b.classList.toggle('selected', b.id === id);
        // b.classList.toggle('selected', b.id === id);
    });
}
boxes.forEach(b => {
    // let id = b.id;
    let id = b.id;
    b.addEventListener('click', e => {
        // history.pushState({id}, `Selected: ${id}`, `./selected=${id}`)
        history.pushState({ id }, `Selected: ${id}`, `./news/${id}`)
        selectBox(id);
    });
});
window.addEventListener('popstate', e => {
    selectBox(e.state.id);
});


// $('#asdf').on('hidden.bs.modal', function () {
//     // revertToOriginalURL();
//     window.addEventListener('popstate', e => {
//         selectBox(e.state.id);
//     });

//     $(this).find('#owl-images').trigger('remove.owl.carousel', imagesss[i])
//     history.replaceState({ id: null }, 'Default state', '../');
//     // alert("The paragraph was clicked.");
    
//     $('.post-media').removeClass("actives")
    
    
// });