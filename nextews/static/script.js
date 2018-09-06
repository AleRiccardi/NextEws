function sticky_relocate() {
    var window_top = $(window).scrollTop();
    var footer_top = $("footer").offset().top;
    var div_top = $('#sticky-sidebar-anchor').offset().top;
    var div_height = $("#sticky-sidebar").height();
    var div_width = $(".sidebar").width();

    var padding = 40;  // tweak here or get from margins etc
    var p_sidebar_up = 20;
    if (window_top + div_height > footer_top - padding) {
        var top_dist = ((window_top + div_height - footer_top + padding)) * -1;
        $('#sticky-sidebar').css({top: top_dist + 20})
    } else if (window_top > (div_top - p_sidebar_up)) {
        $('#sticky-sidebar').addClass('stick');
        $('#sticky-sidebar').css({ width: div_width})
    } else {
        $('#sticky-sidebar').removeClass('stick');
    }
}

$(function () {
    if($("#sticky-sidebar").length) {
        $(window).scroll(sticky_relocate);
        sticky_relocate();
    }
});