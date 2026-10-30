
document.addEventListener("DOMContentLoaded", function() {
  // Select the new sections
  const sections = document.querySelectorAll('.section, .tender-section');

  function checkScroll() {
    const triggerPoint = window.innerHeight * 0.85;

    sections.forEach(section => {
      const content = section.querySelector('.content');
      // For section 2: image, for section 3: image or video-container
      const image = section.querySelector('img, .video-container');
      const sectionTop = section.getBoundingClientRect().top;
      const sectionBottom = section.getBoundingClientRect().bottom;

      if(sectionTop < triggerPoint && sectionBottom > 0) {
        if(content) content.classList.add('active');
        if(image) image.classList.add('active');
      } else {
        if(content) content.classList.remove('active');
        if(image) image.classList.remove('active');
      }
    });
  }

  window.addEventListener('scroll', checkScroll);
  checkScroll(); // trigger on load in case any section is already visible
});


document.addEventListener("DOMContentLoaded", function() {
  // Select all sections you want to animate
  const sections = document.querySelectorAll('.project-visibility, .another-section, .third-section');

  function checkScroll() {
    const triggerPoint = window.innerHeight * 0.85;

    sections.forEach(section => {
      const content = section.querySelector('.content');
      const image = section.querySelector('.image');
      const sectionTop = section.getBoundingClientRect().top;
      const sectionBottom = section.getBoundingClientRect().bottom;

      if(sectionTop < triggerPoint && sectionBottom > 0) {
        content.classList.add('active');
        image.classList.add('active');
      } else {
        content.classList.remove('active');
        image.classList.remove('active');
      }
    });
  }

  window.addEventListener('scroll', checkScroll);
  checkScroll(); // check on load in case any section is visible
});
