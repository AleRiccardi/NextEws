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
            // Start categorizing news
            $.getJSON($SCRIPT_ROOT + '/ajax_categorize_news', {}, function (data) {
                $('.amd-loading-dwn-news').fadeOut("slow", function () {
                    $('.adm-finish').fadeIn("slow");
                });
                Object.keys(data).forEach(function (key) {
                    var record = data[key];
                    var checkBox = `
                            <tr>
                                <th scope="row">${key + 1}</th>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                       ${record.title}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${record.description}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${record.content}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                        <a href="${record.url}">
                                            ${record.url}
                                        </a>
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         <a href="${record.url_to_image}">
                                            ${record.url_to_image}
                                        </a>
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${record.published_at}
                                    </div>
                                </td>
                                <td class="tbl-truncate">
                                    <div class="tbl-truncate-in">
                                         ${record.id_category}
                                    </div>
                                </td>
                            </tr>`;
                    $(checkBox).appendTo('#adm-tbl-news tbody');
                });
            });

        });
    });


});
