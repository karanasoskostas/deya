$('#dateselected li').on('click', function () {
    //alert($(this).text());
    $(this).parent().parent().prev().html($(this).html() + '<span class="caret"></span>');
    selected_index = $(this).closest('li').index();
    //alert(selected_index);
    var now = new moment().format("DD/MM/YYYY");
    document.getElementById("todate").value = now;

    switch (selected_index) {
        case 0:
            now = new moment().format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 1:
            now = new moment().subtract(7, 'days').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 2:
            now = new moment().subtract(15, 'days').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 3:
            now = new moment().subtract(1, 'months').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 4:
            now = new moment().subtract(3, 'months').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 5:
            now = new moment().subtract(6, 'months').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        case 6:
            now = new moment().subtract(12, 'months').format("DD/MM/YYYY");
            document.getElementById("fromdate").value = now;
            break;
        default:
            break;
    }
});
