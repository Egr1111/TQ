function profileFunction() {
  $("#inviteForm").submit(function (e) {
    e.preventDefault();
    $.ajax({
      type: "post",
      url: "/findInvite/",
      data: $(this).serialize(),

      success: function (response) {
        jQuery("<div>", {
          class: "alert alert-primary alert-dismissible fade show",
          role: "alert",
        }).prependTo($(".container"));

        $($(".alert")[0]).text("Запрос отправлен");

        jQuery("<button>", {
          class: "btn-close",
        }).prependTo($(".alert")[0]);

        $($(".alert")[0]).find("button").attr("data-bs-dismiss", "alert");
        $($(".alert")[0]).find("button").attr("aria-label", "Close");
      },

      error: function (jqXHR, textStatus, errorThrown) {
        jQuery("<div>", {
          class: "alert alert-danger alert-dismissible fade show",
          role: "alert",
        }).prependTo($(".container"));

        $($(".alert")[0]).text(errorThrown);

        jQuery("<button>", {
          class: "btn-close",
        }).prependTo($(".alert")[0]);

        $($(".alert")[0]).find("button").attr("data-bs-dismiss", "alert");
        $($(".alert")[0]).find("button").attr("aria-label", "Close");
      },
    });
    return false;
  });
}

$(document).ready(function () {
    profileFunction()
});
