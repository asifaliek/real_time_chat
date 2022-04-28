$(document).on("submit", "form.chat-ajax", function (e) {
    e.preventDefault();
    var $this = $(this);
    var url = $this.attr("action");
    var method = $this.attr("method");
    let data = new FormData(this);
    let users = [];
    $(".groupmodal-users input[type=checkbox]:checked").each(function () {
      users.push(this.value);
    });
  
    data.append("users", JSON.stringify(users));
    jQuery.ajax({
      type: method,
      url: url,
      dataType: "json",
      data: data,
      contentType: false,
      cache: false,
      processData: false,
      success: function (data) {
        let status = data["status"];
        if (status == 200) {
          window.location.reload();
        }
      },
      error: function (data) {},
    });
  });
  