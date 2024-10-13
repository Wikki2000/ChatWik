import { get } from './global/utils.js';

function templates(entity, entityId) {
  return `<div id="entity_${entityId}" class="indie-chats flex">
      <div class="chat-img">
        <img width="40" height="40" src="https://img.icons8.com/plumpy/24/user.png" alt="user"/>
      </div>

      <div id="chat-inner-box" class="indie-chat-inner-box">
        <div class="indie-chat-title-box flex">
          <p class="chat-title">${entity}</p>
          <p></p>
        </div>

        <div class="indie-chat-details flex">
          <p class="chat-snippet"></p>
          <img class="text-status" src="../static/images/sent-tick" alt="sent-tick">
          <p class="unread-count"></p>
        </div>
      </div>
    </div>`
}

$(document).ready(async function() {

  const apiBaseUrl = '/api/v1';

  const allUsers = await get(apiBaseUrl + '/users');
  const userId = localStorage.getItem('userId');

  // Handle clicks on the navigation group
  $('.nav-group').click(function() {
    const clickId = $(this).attr('id');

    // Remove the selected-nav-group class from all navigation bar.
    // Add the selected-nav-group to the nav bar click.
    $('.nav-group').removeClass('selected-nav-group');
    $(this).addClass('selected-nav-group');

    switch (clickId) {
      case 'all-chat': {
        alert("you click all-chat");
        break;
      }
      case 'private-chat': {

        $('#active__chat-section').empty(); // Clear section before appending.


        allUsers.forEach((user, index) => {

          if (userId !== user.id) {
            const userStatus = user.is_active ? `${user.username} (active)` : `${user.username}`;
            $('#active__chat-section').append(templates(userStatus, user.id));
          }

        });
        break;
      }
      case 'group-chat': {
        $('#active__chat-section').empty();
        break;
      }
      default: {
        alert('Unknown option clicked');
      }
    }
  });
});

