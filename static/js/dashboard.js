$(document).ready(function(){
    $('.panel li').click(function(){
        $('.panel li').removeClass('panelclicked');
        $(this).addClass('panelclicked');
    });


});

function carregarPagina(url) {
    $('#main').attr('src', url);
}







