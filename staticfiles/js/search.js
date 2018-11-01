$(function () {
    $search = $('#id_search_field');
    $(".reset").click(function (e) {
        e.preventDefault();
        $search.val("");
        $search.focus();
        return false;
    });
});


var urlParams = new URLSearchParams(window.location.search);

(function ($) {
    $.fn.filter_select = function () {
        if ($('#filter option:selected').text() == 'Filter') {
            $('.search-form').addClass('d-none');
            $('.date-content').removeClass('d-none');
        } else if ($('#filter option:selected').text() == 'Search') {
            $('.search-form').removeClass('d-none');
            $('.date-content').addClass('d-none');
        }
    }
})(jQuery);

$('body').on('change', '#filter', function () {
    $(document).filter_select();
});

$(document).ready(function () {
    if (window.location.href.indexOf("&start_date") > -1) {
        $("#filter option").each(function () {
            if ($(this).text() == 'Filter')
                $(this).attr("selected", "selected");
        });
    }else if (window.location.href.indexOf("&q") > -1) {
        $("#filter option").each(function () {
            if ($(this).text() == 'Search')
                $(this).attr("selected", "selected");
        });
    }

    $(document).filter_select();


    $('#start_date_nep').nepaliDatePicker({
      npdMonth: true,
      npdYear: true,
      ndpEnglishInput: 'start_date',
      onChange: function(){
        $('#end_date_nep').nepaliDatePicker({
          npdMonth: true,
          npdYear: true,
          ndpEnglishInput: 'end_date',
          disableBefore: changeFormat($('#start_date_nep').val()),
        });
      }
    });

    $('#end_date_nep').nepaliDatePicker({
      npdMonth: true,
      npdYear: true,
      ndpEnglishInput: 'end_date'
    });


    if(urlParams.get('start_date')){
      $("#start_date_nep").val(AD2BS(urlParams.get('start_date')));
      $("#start_date").val(urlParams.get('start_date'));
      var dateConvert = AD2BS(urlParams.get('start_date'));
      $('#end_date_nep').nepaliDatePicker({
        npdMonth: true,
        npdYear: true,
        ndpEnglishInput: 'end_date',
        disableBefore: changeFormat(dateConvert),
      });
    }

    if(urlParams.get('end_date')){
      $("#end_date_nep").val(AD2BS(urlParams.get('end_date')));
      $("#end_date").val(urlParams.get('end_date'));
    }
});

function changeFormat(date){
  var splitDate = date.split("-");
  return splitDate[1] + "/" + (parseInt(splitDate[2])) + "/" + splitDate[0];
}
