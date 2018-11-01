$(document).ready(function(){
  // helps to stop double clicking of submit button
    var myButton = $('#submit-btn');  // your button ID here
    myButton.on('click', function(){
        myButton.prop('disabled', true);
    });

// for formset as well as deleting file in formset_tags
  jQuery(function($) {
      $("#formset").formset({
          reorderMode: 'dom',
      });

      $('#formset').on('formAdded', function(event){
          alert("yes");
      });


  });


  $('body').on('click','.photo-delete',function(){
    deleteButton = $(this);

    fileID = deleteButton.attr('id');

    $.ajax({
      url: '/home-road-certifications/delete-file-api/' + fileID + '/',
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        deleteButton.closest('div').remove();
      },
      type: 'GET'
    });
  });

// for deleting image form
    $('body').on('click', '.delete-form',function(){
      btn = $(this);
      prefix = btn.attr('id');
      var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (total > 0){
          btn.closest('div').remove();
          var forms = $('.delete-form');
          $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
          for (var i=0, formCount=forms.length; i<formCount; i++) {
              $(forms.get(i)).find(':input').each(function() {
                  updateElementIndex(this, prefix, i);
              });
          }
      }
      return false;
      form.remove();
    });
});

// for making category active in menu
$(document).ready(function(){
  var pathname = window.location.pathname.split("/")[1];
  if(pathname){
    $("li").each(function(){
      var id =$(this).attr('id');
      if(pathname == id ){
        $(this).attr("class", "active");
        $(this).find("a").attr("class","toggled");
        var parent = $(this).closest("#id_parent");
        parent.attr("class", "active");
        parent.find('a.menu-toggle').attr("class", "menu-toggle toggled");
        parent.find('ul.ml-menu').css('display', 'block');
      }
    })
  }else{
    $('#id_home').attr("class", "active")
  }

  $('#id_nep_date').val(todayNepaliDate());
  $('#id_eng_date').val(todayEnglishDate());

});

// preventing textbox from generating extra datepicker
function changeFormat(date){
  var splitDate = date.split("-");
  return splitDate[1] + "/" + (parseInt(splitDate[2])) + "/" + splitDate[0];
}

$('body').on('click','.calender-btn',function () {
    $('#id_nep_date').nepaliDatePicker({
        npdMonth: true,
        npdYear: true,
        ndpEnglishInput: 'id_eng_date',
        disableBefore: changeFormat(todayNepaliDate()),
        disableAfter: changeFormat(todayNepaliDate()),
        onChange: function(){
          $('#ndp-nepali-box').remove();
        }
    });
    showNdpCalendarBox("id_nep_date");
});

function todayEnglishDate(){
  var d = new Date();
  var day = d.getUTCDate();
  var month = parseInt(d.getUTCMonth()) + 1 ;
  var year = d.getUTCFullYear();
  return year + "-" + month + "-" + day;
}

function todayNepaliDate(){
  return AD2BS(todayEnglishDate());
}



// };
// $(function () {
//     $.Admin.leftSideBar.activate();
//     $.Admin.leftSideBar.checkStatusForResize();
//     var $body = $('body');
//     var $openCloseBar = $('.navbar .bars');
//     var width = $body.width();
//     closebutton = $('.close_button');
//     openbutton = $('.open_button');


//     sessiondata = sessionStorage.getItem("sidebar");

//     if (sessiondata !== null){
//         if(sessiondata == 'closed'){
//             $body.addClass('ls-closed');
//         }

//     }

//       openbutton.on('click tap',function(){
//         $body.addClass('ls-closed');
//         if (typeof(Storage) !== "undefined") {
//             sessionStorage.setItem("sidebar", "closed");

//         }
//         openbutton.addClass('hidden')
//         closebutton.removeClass('hidden')

//         });

//         closebutton.on('click tap',function(){
//             $body.removeClass('ls-closed');
//             if (typeof(Storage) !== "undefined") {
//                 sessionStorage.setItem("sidebar", "open");

//             }
//             closebutton.addClass('hidden')
//             openbutton.removeClass('hidden')

//         });

//     //   $(document).keyup(function(e) {
//     //     if (e.keyCode === 27) {
//     //       toggleSidebar();
//     //     }

//     //     });


// <button class="close_button"><i class="fa fa-minus" ></i></button>
//         <button class="open_button hidden" > <i class="fa fa-plus"></i></button>




// });
