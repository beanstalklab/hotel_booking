$('input[type=file]').change(function(e) {
    $in = $(this);
    $in.next().html($in.val());
    
});

$('.uploadButton').click(function() {
    var fileName = $("#fileUpload").val();
    if (fileName) {
        alert(fileName + " can be uploaded.");
    }
    else {
        alert("Please select a file to upload");
    }
});