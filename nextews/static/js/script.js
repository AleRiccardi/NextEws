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
        $.getJSON($SCRIPT_ROOT + '/ajax_news_process', {}, function (data) {
            var num_news = 0;

            Object.keys(data).forEach(function (key) {
                var record = data[key];
                var content = record.content.replace(/<br>/g, '')
                var checkBox = `
                        <tr>
                            <th scope="row">${parseInt(key) + 1}</th>
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
                                     ${content}
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
                                     ${record.category}
                                </div>
                            </td>
                        </tr>`;
                $(checkBox).appendTo('#adm-tbl-news tbody');
                num_news++;
            });

            if (num_news != 0) {
                $('#num_news_added').text(num_news);
                $('.amd-loading-dwn-news').fadeOut("slow", function () {
                    $('.adm-finish').fadeIn("slow");
                });
            } else {
                $('.amd-loading-dwn-news').fadeOut("slow", function () {
                    $('.adm-no-news').fadeIn("slow");
                });
            }

        });
    });


    $('#btn_reset_process').bind('click', function () {
        $('.adm-finish').fadeOut("slow", function () {
            $('.jumbotron-admin').removeClass('jmb-adm-restrict');
            $('.adm-intro').addClass('show');
            $('#adm-tbl-news tbody').html('');
        });
    });

    $('#btn_reset_process_no_news').bind('click', function () {
        $('.adm-no-news').fadeOut("slow", function () {
            $('.jumbotron-admin').removeClass('jmb-adm-restrict');
            $('.adm-intro').addClass('show');
            $('#adm-tbl-news tbody').html('');
        });
    });
});
