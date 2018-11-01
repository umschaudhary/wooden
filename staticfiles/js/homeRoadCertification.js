// home road certification create js
// $(document).ready(function(){
//   $('#id_district').empty().append('<option value selected>जिल्ला</option>');
//   $('#id_local_body').empty().append('<option value selected>गा. वि. स. / न. पा </option>');
// });

$('body').on('change','#id_state', function(){
  var selected_value = $(this).children('option:selected').val();
  if(selected_value){
    $.ajax({
      url: '/districts/get-options/?state=' + selected_value,
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        console.log(data);

        $('#id_district').removeAttr('disabled').empty().append(data);
        $('#id_local_body').attr('disabled', true).empty().append('<option value selected>गा. वि. स. / न. पा </option>');
        $('#id_ward_no').attr('disabled', true).val('');
      },
      type: 'GET'
    });
  }else{
    $('#id_district').attr('disabled', true).html('<option value selected>जिल्ला</option>').val('');
    $('#id_local_body').attr('disabled', true).empty().append('<option value selected>गा. वि. स. / न. पा </option>').val('');
    $('#id_ward_no').attr('disabled', true).val('');
  }
});

$('body').on('change','#id_district', function(){
  var selected_value = $(this).children('option:selected').val();
  if(selected_value){
    $.ajax({
      url: '/local-bodies/get-options/?district=' + selected_value,
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        console.log(data);
        $('#id_local_body').removeAttr('disabled').empty().append(data);
      },
      type: 'GET'
    });
  }else{
    $('#id_local_body').attr('disabled', true).empty().append('<option value selected>गा. वि. स. / न. पा </option>').val('');
    $('#id_ward_no').attr('disabled', true).val('');
  }
});

$('body').on('change','#id_local_body', function(){
  var selected_value = $(this).children('option:selected').val();
  if(selected_value){
    $('#id_ward_no').removeAttr('disabled');
  }else{
    $('#id_ward_no').attr('disabled', true).val('');;
  }
});

$('body').on('change','.old_place', function(){
  var selected_value = $(this).children('option:selected').val();
  var select = $(this).parents('tr').find('.new-name');
  if(selected_value){
    $.ajax({
      url: '/old-and-present-places/new-place-data/?old_place=' + selected_value,
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        select.val(data['new_place'])
      },
      type: 'GET'
    });
  }else{
    // $('#id_local_body').html('<option value selected>गा. वि. स. / न. पा </option>')
  }
});

$('body').on('change','.home-checkbox', function(){
  var home_type = $(this).parents('tr').find('.home-type');
  var estimated_cost =  $(this).parents('tr').find('.estimated-cost');
  if($(this).is(":checked")){
    $.ajax({
      url: '/type-of-houses/api',
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        home_type.removeAttr('disabled').empty().append(data);
        estimated_cost.removeAttr('disabled');
      },
      type: 'GET'
    });
  }else{
    home_type.attr('disabled', true).empty().append('<option value selected>छान्नुहोस</option>');
    estimated_cost.val('').attr('disabled', true);
  }
});

$('body').on('change','.road-checkbox', function(){
  var road_type = $(this).parents('tr').find('.road-type');
  if($(this).is(":checked")){
    $.ajax({
      url: '/road-types/api',
      cache: false,
      error: function () {
        console.log("error");
      },
      success: function (data) {
        road_type.removeAttr('disabled').empty().append(data);
      },
      type: 'GET'
    });
  }else{
    road_type.attr('disabled', true).empty().append('<option value selected>छान्नुहोस</option>');
  }
});
