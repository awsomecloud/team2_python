$(function() {

  $("#contactForm input,#contactForm textarea").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM akey skey vpcTag regionid filename servicelist
      var akey = $("input#akey").val();
      var skey = $("input#skey").val();
      var vpctag = $("input#vpctag").val();
      var regionid = $("select#regionid").val();
      var filename = $("input#filename").val();
      var servicelist = $("select#servicelist").val();
      var firstName = "name"; // For Success/Failure Message

      // 버튼 이벤트 발생시 엑셀 변환중 메세지 띄우기
      $('#success').html("<div class='alert alert-success'>");
      $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
        .append("</button>");
      $('#success > .alert-success')
        .append("<strong>검색 중 입니다... </strong>");
      $('#success > .alert-success')
        .append('</div>');
      // Check for white space in name for Success/Fail message
      // if (firstName.indexOf(' ') >= 0) {
      //   firstName = name.split(' ').slice(0, -1).join(' ');
      // }
      $this = $("#sendMessageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "https://0wwngh8nd0.execute-api.ap-northeast-2.amazonaws.com/test/",
        type: "POST",
        data: {
          akey: akey,
          skey: skey,
          vpctag: vpctag,
          regionid: regionid,
          filename: filename,
          servicelist: servicelist
        },
        cache: false,

        success: function(result) {
          // Success message
          $('#success').html("<div class='alert alert-success'>");
          $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-success')
            .append("<strong>Excel 파일 다운로드가 시작 되었습니다. </strong>");
          $('#success > .alert-success')
            .append('</div>');
          //clear all fields
          var link = document.createElement("a");
          document.body.appendChild(link);
          link.setAttribute("type", "hidden");
          link.href = "data:text/plain;base64," + result;
          link.download = filename + ".xlsx";
          link.click();
          document.body.removeChild(link);
          $('#contactForm').trigger("reset");
        },
        error: function() {
          // Fail message
          $('#success').html("<div class='alert alert-danger'>");
          $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-danger').append($("<strong>").text("실패하였습니다. 관리자에게 문의 바랍니다."));
          $('#success > .alert-danger').append('</div>');
          //clear all fields
          $('#contactForm').trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // AJAX 완료 후 버튼 3초 대기 후 버튼 활성화
          }, 3000);
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});
