function loginFunctions(params) {
  $("input[name='phone']").on("input", function () {
    if ($("#enter-phone").find("p").length == 2) {
      console.log(0);
      $("#enter-phone").find($("p")[1]).remove();
      $("#repeat").remove();
      $("#enter-phone").find(".row").find("button").text("Подтвердить номер");
    }
    if ($(this).val() != "+" && $(this).val().length == 1) {
      $(this).val(parseInt($(this).val()) - 1);
    }
    if ($(this).val() < 0) {
      $(this).val(0);
    }
  });

  $("#enter-phone")
    .find(".row")
    .find("button")
    .on("click", function () {
      $.ajax({
        type: "post",
        url: "/phoneHTML/",
        data: $("#enter-phone").serialize(),
        success: function (response) {
          if ($("#enter-phone").find("p").length == 1) {
            $("#enter-phone").append(response);
            $("#enter-phone").find(".row").remove();

            jQuery("<div>", {
              id: "success",
              class:
                "row justify-content-center align-items-center g-2 text-center",
            }).appendTo($(".container"));
            jQuery("<button>", {
              class: "btn btn-primary",
            }).appendTo($("#success"));

            $("#success").find("button").text("Отправить код");

            jQuery("<div>", {
              id: "repeat",
              class:
                "row justify-content-center align-items-center g-2 text-center",
            }).appendTo($(".container"));

            jQuery("<button>", {
              type: "button",
              class: "btn btn-danger",
            }).appendTo($("#repeat"));

            $("#repeat").find("button").text("Заново подтвердить номер");
            $("#repeat")
              .find(".btn-danger")
              .on("click", function (e) {
                $.ajax({
                  type: "post",
                  url: "/phone/",
                  data: $("#enter-phone").serialize(),
                  success: function (response) {
                    jQuery("<div>", {
                      class: "alert alert-primary alert-dismissible fade show",
                      role: "alert",
                    }).prependTo($(".container"));

                    $($(".alert")[0]).text("Клд был снова отправлен");

                    jQuery("<button>", {
                      class: "btn-close",
                    }).prependTo($(".alert")[0]);

                    $($(".alert")[0])
                      .find("button")
                      .attr("data-bs-dismiss", "alert");
                    $($(".alert")[0])
                      .find("button")
                      .attr("aria-label", "Close");
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

                    $($(".alert")[0])
                      .find("button")
                      .attr("data-bs-dismiss", "alert");
                    $($(".alert")[0])
                      .find("button")
                      .attr("aria-label", "Close");
                  },
                });
                return false;
              });
            $("#success")
              .find(".btn-primary")
              .on("click", function (e) {
                $.ajax({
                  type: "post",
                  url: "/loginCode/",
                  data: $("#enter-phone").serialize(),
                  success: function (response) {
                    console.log(response);
                    window.location.href = "http://" + window.location.host + "/profile/";                  },
                  error: function (jqXHR, textStatus, errorThrown) {
                    jQuery("<div>", {
                      class: "alert alert-danger alert-dismissible fade show",
                      role: "alert",
                    }).prependTo($(".container"));

                    $($(".alert")[0]).text(errorThrown);

                    jQuery("<button>", {
                      class: "btn-close",
                    }).prependTo($(".alert")[0]);

                    $($(".alert")[0])
                      .find("button")
                      .attr("data-bs-dismiss", "alert");
                    $($(".alert")[0])
                      .find("button")
                      .attr("aria-label", "Close");
                  },
                });
                return false;
              });
          }
        },
      });
    });

  $("#enter-phone").on("submit", function (e) {
    e.preventDefault();
    $.ajax({
      type: "post",
      url: "/phone/",
      data: $(this).serialize(),
      success: function (response) {
        console.log(response);
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
  loginFunctions();
});
