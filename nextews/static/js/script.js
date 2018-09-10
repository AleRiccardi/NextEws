/************************************************

 JAVASCRIPT File

 ************************************************/


/**
 * Relocate the side-bar when occur.
 */
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
        $('#sticky-sidebar').css({width: div_width})
    } else {
        $('#sticky-sidebar').removeClass('stick');
    }
}

$(function () {
    /* Call the sidebar sticky function */
    if ($("#sticky-sidebar").length) {
        $(window).scroll(sticky_relocate);
        sticky_relocate();
    }


    $('#btn_dwn_news').bind('click', function () {
        $('.jumbotron-admin').addClass('jmb-adm-restrict');
        $('.adm-intro').removeClass('show');
        $('.amd-loading-dwn-news').fadeIn("slow");

        // Start downloading news
        $.getJSON($SCRIPT_ROOT + '/ajax_scan_news', {}, function (data) {
            $('.adm-num-ctg-news').text(data.num_news_to_categorize)
            $('.amd-loading-dwn-news').fadeOut("slow", function () {
                $('.amd-loading-ctg-news').fadeIn("slow");
            });
            // Start categorizing news
            $.getJSON($SCRIPT_ROOT + '/ajax_categorize_news', {}, function (data) {
                for (var i = 0; i < data.length; i++) {
                    var checkBox = `
                            <tr>
                                <td scope="row" class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                       ${data[i].title}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].description}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].content}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].url}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].url_to_image}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].published_at}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${data[i].id_category}
                                    </div>
                                </td>
                            </tr>`;
                    $(checkBox).appendTo('#adm-tbl-news tbody');
                }
                $('.amd-loading-ctg-news').fadeOut("slow", function () {
                    $('.adm-finish').fadeIn("slow");
                });
            });

        });
    });


});
