$(function(){
    $('#create-car-modal-form').on('submit', function(e){
        e.preventDefault();
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/car', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send($('#create-car-modal-form').serialize());
        console.log('oi')
        // $.ajax({
        //     url: '/car', 
        //     type: 'POST', 
        //     data: $('#create-car-modal-form').serialize(),
        //     success: function(data){
        //          alert('successfully submitted')
        //     }
        // });
    });
  });