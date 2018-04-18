
$( function() {
    $( document ).tooltip();
});
$( "#bill" ).click(function( event ) {
    clear();
    var source = $('#inputSource').val();
    if(source == ''){
        alert('Por Favor insira um Numero de Telefone!')
    }
    var period = $('#periodDate').val();
    if(period == undefined){
        period = ''
    }
    $.ajax({
      url: "/api/v1/get_phone_bill/?source="+source+"&period="+period,
      success: function(data) {
          if (data['calls'].length == 0) {
              $('#notAccount').show();
              $('#detailAccount').hide();
          }
          else {
              $('#notAccount').hide();
              $('#detailAccount').show();
              $.each(data['calls'], function (key, value) {
                  var detail = '<tr>' +
                      '<td>' + key + '</td>' +
                      '<td>' + value['destination'] + '</td>' +
                      '<td>' + value['start_date'] + '</td>' +
                      '<td>' + value['start_time'] + '</td>' +
                      '<td>' + value['call_duration'] + '</td>' +
                      '<td>' + value['price'] + '</td>' +
                      '</tr>';
                  $('table>tbody').append(detail);
              });
              $('#phoneNumber').html(source);
              $('#period').html(data['period']);
              $('#amountAccount').html(data['amount']);
          }
      }
    });
    event.preventDefault();
});
function clear(){
  $('#phoneNumber').html('');
  $('#period').html('');
  $('#amountAccount').html('');
  $('table>tbody').html('');
}