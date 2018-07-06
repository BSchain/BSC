function commentData(obj) {
    data_rating =  $('#data_rating').val();
    rating_data_id = $('#rating_data_id').val();
    $.ajax("/Order/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "rating_data_id": rating_data_id,
            "data_score": data_rating,
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              // alert(data.message)
              window.location.replace("/Order/");
          }
      })
    return;
}