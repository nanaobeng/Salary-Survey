
    (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  try {
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: (target.offset().top - 72)
          }, 1000, "easeInOutExpo");
          return false;
        }
      }
    });
  } catch (error) {
    
  }
  
  try {
     // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });
  } catch (error) {
    
  }
 

  // Activate scrollspy to add active class to navbar items on scroll
  try {
    $('body').scrollspy({
      target: '#mainNav',
      offset: 75
    });
  } catch (error) {
    
  }
  

  // Collapse Navbar
  try {
    var navbarCollapse = function() {
      if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-scrolled");
        $("#logo").removeClass("white_logo");
        $("#logo").addClass("black_logo");
      } else {
        $("#mainNav").removeClass("navbar-scrolled");
        $("#logo").addClass("white_logo");
        $("#logo").removeClass("black_logo");
      }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
  } catch (error) {
    
  }
 
  //datatable for admin view surveys

  try {
    $(document).ready(function() {
      var surveysTable =  $('#surveys').DataTable({sDom: 'lrtip', 'bLengthChange': false});
      $('#search_survey').keyup(function(){
        surveysTable.search($(this).val()).draw() ;
  })

} );
  } catch (error) {
    
  }

  //datatable for service requests
  try{
  $(document).ready(function() {
  
  var requestsTable = $('#all_requests_table').DataTable({sDom: 'lrtip', 'bLengthChange': false});
  
  $('.filter').on('change', function() {

    var val = $(this).val();
    var checked = $(this).prop('checked');
    var index = filtered.indexOf( val );
    
    if (checked && index === -1) {
      filtered.push(val);
    } else if (!checked && index > -1) {
      filtered.splice(index, 1);
    }
    requestsTable.draw();
  });
  $('#filter_corporate').prop('checked', true)
  $('#filter_corporate').trigger('change')
  $('#filter_individual').prop('checked', true)
  $('#filter_individual').trigger('change')
    $('#search_request').keyup(function(){
        requestsTable.search($(this).val()).draw() ;
    })

    } );
 
  } catch (error) {
    
  }

   //datatable for client_benchmark_jobs and clients

   try {
    
    $(document).ready(function() {
     
      var surveysTable =  $('#my_benchmark_jobs').DataTable({sDom: 'lrtip', 'bLengthChange': false});
      $('#search_job').keyup(function(){
        surveysTable.search($(this).val()).draw() ;
  })
  var clientsTableCorporate =  $('#admin_all_clients_corporate').DataTable({sDom: 'lrtip', 'bLengthChange': false});
      $('#search_client').keyup(function(){
        clientsTableCorporate.search($(this).val()).draw() ;
      })
      var clientsTableIndividual =  $('#admin_all_clients_individual').DataTable({sDom: 'lrtip', 'bLengthChange': false});
      $('#search_client').keyup(function(){
        clientsTableIndividual.search($(this).val()).draw() ;
      })
} );
  } catch (error) {
    
  }

  //resize benchmark jobs textarea

  $('.benchmark_job_textarea').on('focus', function(){
    $(this).addClass('textarea_expand')
    })
    $('.benchmark_job_textarea').on('focusout', function(){
        $(this).removeClass('textarea_expand')
    })

    //trigger file upload for benchmark jobs
    $('#upload_jobs_btn').on('click', function(){
      $('#upload_jobs_file').trigger('click')
    })

    //Modal events for client job benchmarking

    $('#job_not_applicable').change(function() {
        if($(this).is(":checked")) {
          $('#proceed_btn').hide();     
           $('#save_btn').show(); 
        }
        else{
          $('#proceed_btn').show();     
        $('#save_btn').hide(); 
        }
            
    });

    // Events for admin create survey form

    $("#add_benchmark").click(function(){
      $("#selected_benchmark").append(`<li class="list-group-item d-flex justify-content-between align-items-center">
        Finance Manager
        <i class="fas fa-trash benchmark-trash"></i>
      </li>`);
    
  });
$(".review_survey_btn").click(function(){
  
  $("#review_survey_name").html($("#survey_name").val())
  $("#review_client_name").html($("#client").val())
  $("#review_industry").html($("#industry").val())
  $("#review_area_of_operation").html($("#area_of_operation").val())
  $("#review_start_date").html($("#start_date").val())
  //append selected benchmark jobs to modal
  var selected_jobs = $('#selected_benchmark').children('li');
  $('#review_benchmark_jobs').empty()
  selected_jobs.each(function(){
    var item = $(this)[0].firstChild     
   $('#review_benchmark_jobs').append('<li>'+item.nodeValue+'</li>');
  })
  //Append selected comparators to modal
  var selected_comparators = $('#selected_comparators').children('li');
  $('#review_comparators').empty()
  selected_comparators.each(function(){
    var item = $(this)[0].firstChild     
   $('#review_comparators').append('<li>'+item.nodeValue+'</li>');
  })

})
    
})(jQuery); // End of use strict
