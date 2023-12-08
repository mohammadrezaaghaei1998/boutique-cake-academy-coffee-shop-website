// education gallery

$(document).ready(function(){
    for (var i=1; i <= $('.slider__slide').length; i++){
      $('.slider__indicators').append('<div class="slider__indicator" data-slide="'+i+'"></div>')
    }
    setTimeout(function(){
      $('.slider__wrap').addClass('slider__wrap--hacked');
    }, 1000);
  })
  
  function goToSlide(number){
    $('.slider__slide').removeClass('slider__slide--active');
    $('.slider__slide[data-slide='+number+']').addClass('slider__slide--active');
  }
  
  $('.slider__next, .go-to-next').on('click', function(){
    var currentSlide = Number($('.slider__slide--active').data('slide'));
    var totalSlides = $('.slider__slide').length;
    currentSlide++
    if (currentSlide > totalSlides){
      currentSlide = 1;
    }
    goToSlide(currentSlide);
  })






  document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll(".nav li a");
    const contentSections = document.querySelectorAll(".content-section");

    navLinks.forEach((link, index) => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            
            // Hide all content sections
            contentSections.forEach(section => {
                section.style.display = "none";
            });

            // Display the corresponding content section
            contentSections[index].style.display = "block";
        });
    });
});





document.addEventListener("DOMContentLoaded", function() {
  const navLink = document.querySelector('li.dropdown a[href="#hakkımızda"]');
  
  if (navLink) {
    navLink.addEventListener("click", scrollToHakkimizda);
  }
  
  function scrollToHakkimizda(e) {
    e.preventDefault();
    const targetSection = document.querySelector("#hakkımızda");
    
    if (targetSection) {
      const offsetTop = targetSection.offsetTop;
      const scrollOptions = {
        behavior: "smooth"
      };
      
      if ("scrollBehavior" in document.documentElement.style) {
        // Use native smooth scrolling if supported
        window.scrollTo({
          top: offsetTop,
          ...scrollOptions
        });
      } else {
        // Use a JavaScript-based scroll animation as a fallback
        scrollSmoothly(offsetTop, scrollOptions);
      }
    }
  }

  function scrollSmoothly(offsetTop, options) {
    const start = window.pageYOffset;
    const duration = options.duration || 500; // Adjust the duration as needed
    const startTime = "now" in window.performance ? performance.now() : new Date().getTime();
    
    function step(currentTime) {
      const elapsedTime = currentTime - startTime;
      const progress = Math.min(elapsedTime / duration, 1);
      
      window.scrollTo(0, start + offsetTop * progress);
      
      if (progress < 1) {
        requestAnimationFrame(step);
      }
    }

    requestAnimationFrame(step);
  }
});




// Home // srvice(müşteri memnuniyeti-pastalar-kahveler-toplam ürün sayısı)
function animateValue(element, start, end, duration) {
  let startTime;

  function update(currentTime) {
    if (!startTime) startTime = currentTime;
    const progress = Math.min((currentTime - startTime) / duration, 1);
    const value = Math.floor(progress * (end - start) + start);
    element.textContent = value;
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

const elements = document.querySelectorAll('.number');

elements.forEach((element) => {
  const endValue = parseInt(element.getAttribute('data-number'));
  animateValue(element, 0, endValue, 10000);
});






//tuggle for change_password_dashboard
document.addEventListener('DOMContentLoaded', function () {
  const toggleButtons = document.querySelectorAll('.toggle-password');

  toggleButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      const targetInput = document.getElementById(targetId);

      if (targetInput.type === 'password') {
        targetInput.type = 'text';
        this.classList.remove('fa-eye');
        this.classList.add('fa-eye-slash');
        targetInput.classList.add('small-font');
      } else {
        targetInput.type = 'password';
        this.classList.remove('fa-eye-slash');
        this.classList.add('fa-eye');
        targetInput.classList.remove('small-font');
      }
    });
  });
});









//drop down payment address

(function($) {
  var RadioDropdown = function(el) {
      var _this = this;
      this.isOpen = false;
      this.areAllChecked = false;
      this.$el = $(el);
      this.$label = this.$el.find('.dropdown-label');
      this.$checkAll = this.$el.find('[data-toggle="check-all"]').first();
      this.$inputs = this.$el.find('[type="radio"]');
    
      this.onRadioChange();
    
      this.$label.on('click', function(e) {
          e.preventDefault();
          _this.toggleOpen();
      });
    
      this.$checkAll.on('click', function(e) {
          e.preventDefault();
          _this.onCheckAll();
      });
    
      this.$inputs.on('change', function(e) {
          _this.onRadioChange();
      });
  };
  
  RadioDropdown.prototype.onRadioChange = function() {
      this.updateStatus();
  };
  
  RadioDropdown.prototype.updateStatus = function() {
      var checked = this.$el.find(':checked');
    
      this.areAllChecked = false;
      this.$checkAll.html('Check All');
    
      if(checked.length === 0) {
          this.$label.html('Select');
      } else {
          this.$label.html(checked.parent('label').text());
      }
  };
  
  RadioDropdown.prototype.onCheckAll = function() {
      this.$inputs.prop('checked', true);
      this.updateStatus();
  };
  
  RadioDropdown.prototype.toggleOpen = function(forceOpen) {
      var _this = this;
    
      if(!this.isOpen || forceOpen) {
          this.isOpen = true;
          this.$el.addClass('on');
          $(document).on('click', function(e) {
              if(!$(e.target).closest('[data-control]').length) {
                  _this.toggleOpen();
              }
          });
      } else {
          this.isOpen = false;
          this.$el.removeClass('on');
          $(document).off('click');
      }
  };
  
  var radioDropdowns = document.querySelectorAll('[data-control="checkbox-dropdown"]');
  for(var i = 0, length = radioDropdowns.length; i < length; i++) {
      new RadioDropdown(radioDropdowns[i]);
  }
})(jQuery);