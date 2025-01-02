import { ajaxRequest, getBaseUrl, get } from '../global/utils.js';

function friendSectionTemplate(
  userData, timeStamp = 'Just now',
  acceptBottonContent = 'Add',
  rejectButtonContent = 'Cancel'
) {
  return `<li id="chat_${userData.id}" class="chat-list">
    <a href="#">
      <div class="chat-list-image online">
        <img src="/static/images/profile_photo_placeholder.jpeg" alt="Profile Photo" class="dashboard__user-avatar">
      </div>

      <div class="chat-details">
        <h4 id="name" class="name">${userData.username}</h4>
        <p class="accept__reject-btns">
           <button data-id="${userData.id}" class="btn btn-success">${acceptBottonContent}</button>
           <button data-id="${userData.id}"class="btn btn-danger reject">${rejectButtonContent}</button>
         </p>
       </div>

       <div class="content">
         <h6 class="content-timestamp">${timeStamp}</h6>
       </div>
     </a>
   </li>
  `
}

$(document).ready(function() {
  const API_BASE_Url = getBaseUrl()['apiBaseUrl'];
  const APP_BASE_Url = getBaseUrl()['appBaseUrl'];

  // Always highlight the "Your Friends" button as default
  // and unselect the others button when click on friends icon.
  $('#friends__list-click').addClass('dashboard__highlight-item');

  /*============== Load Friend profile pages =================*/
  $('#dashboard__main-dynamic').on('click', '.user-friends', function() {
    const friendId = $(this).attr('id').split('_')[1];
    window.location.href = APP_BASE_Url + `/friends/${friendId}/profile`;
  });

  /*===== Load Friends of User =======*/
  function load() {
    $('#friends__dynamic').empty();
    const url = API_BASE_Url + '/friends';
    $.get(url, function(friends) {
      friends.forEach((friend) => {
        console.log(friend);
        const userData = { username: friend.username, id: friend.id };
        $('#friends__dynamic').append(friendSectionTemplate(userData));
        $('.btn, .content-timestamp').remove();

        // Add a unique class when loading user friends this help to show
        // friends profile section only on "Your friends dashboard section
        $('.chat-list').addClass('user-friends');

      });
    });
  }
  $('#dashboard__main').on('click', '#dashboard__main-freind', function() {
    $('#friends__list-click').addClass('dashboard__highlight-item');
    load();
  });

  $('#dashboard__main-dynamic').on('click', '#friends__list-click', function() {
    $(this).addClass('dashboard__highlight-item');
    $('#friends__suggestion-click, #requests__list-click').removeClass('dashboard__highlight-item');
    load();
  });

  /*===== Load Suggested Friends to User =======*/
  $('#dashboard__main-dynamic').on('click', '#friends__suggestion-click', async function() {
    $(this).addClass('dashboard__highlight-item');
    $('#friends__list-click, #requests__list-click').removeClass('dashboard__highlight-item');

    $('#friends__dynamic').empty();

    // Display suggested friends base on location
    try {
      const url = API_BASE_Url + '/friends-suggestion';
      const friends = await get(url);
      console.log(friends);
      friends.forEach((friend) => {
        const userData = { username: friend.username, id: friend.id };

        // Skip if user has recieve request already from friend.
        // This should be display when friend req list btn is click.
        if (friend.is_sent) {
          $('#friends__dynamic').append(friendSectionTemplate(userData, null, 'Cancel', null));
          $(`[data-id="${friend.id}"]`).removeClass('btn-success');
          $(`[data-id="${friend.id}"]`).addClass('btn-danger');
        } else {
          $('#friends__dynamic').append(friendSectionTemplate(userData, null, 'Add', null));
        }

        $('.content-timestamp').remove();
        $('.reject').remove(); // Use only one button for meet new friend section
      });
    } catch(error) {
      console.log(error);
    }
    // Set the input field of friend freinds-dashboard.html to sent
    // This is to handle sent or accept, since both use same button.
    $('#friends__accept-sent').val('sent');
  });

  /*============ Accept or Send Friend Request ====================*/
  $('#dashboard__main-dynamic').on('click', '.btn-success', function() {
    const friendId = $(this).data('id');
    const sentOrAccept = $('#friends__accept-sent').val();
    const sentUrl = `${API_BASE_Url}/friends/${friendId}/sent-request`;
    const acceptUrl = `${API_BASE_Url}/friends/${friendId}/accept-request`;

    const method = sentOrAccept === 'accept' ? 'PUT' : 'POST';
    const url = sentOrAccept === 'accept' ? acceptUrl : sentUrl;

    const $btnClick = $(this);

    $btnClick.text('.....');
    ajaxRequest(url, method, null,
      (response) => {
        $btnClick.removeClass('btn-success');
        $btnClick.addClass('btn-danger');
        $btnClick.text('Cancel');
        if (sentOrAccept === 'accept') {
          $btnClick.closest('li').remove();
          alert('Request Accepted');
        }
      },
      (error) => {
        if (error.status) {
          alert(error.responseJSON.error);
        } else {
          console.log(error);
        }
      }
    );
  });
  /*============= Cancel friend request ================*/
  $('#dashboard__main-dynamic').on('click', '.btn-danger', function() {
    const $clickBtn = $(this);
    const friendId =  $clickBtn.data('id');
    $clickBtn.text('......');
    const url =  API_BASE_Url + `/friends/${friendId}/cancel-request`;
    ajaxRequest(url, 'DELETE', null,
      (response) => {
        if (response.status === 'Success') {
          $clickBtn.removeClass('btn-danger');
          $clickBtn.addClass('btn-success');
          $clickBtn.text('Add');
        }
      },
      (error) => {
        console.log(error);
      }
    );
  });
  /*============= Load user friends request list ================*/
  $('#dashboard__main-dynamic').on('click', '#requests__list-click', async function() {
    $(this).addClass('dashboard__highlight-item');
    $('#friends__list-click, #friends__suggestion-click').removeClass('dashboard__highlight-item');

    // Empty the recent data and append current one.
    $('#friends__dynamic').empty();
    try {
      const url = API_BASE_Url + '/friends-request';
      const friends = await get(url);
      console.log(friends);
      friends.forEach((friend) => {
        const userData = { username: friend.username, id: friend.id };
        $('#friends__dynamic').append(friendSectionTemplate(userData, null, 'Accept'));
        $('.content-timestamp').remove();

      });
    } catch(err) {
      console.log(err);
    }
    $('#friends__accept-sent').val('accept');
  });


  /*============= Load message list of friends ================*/
  async function messageList() {
    try {
      const url = API_BASE_Url + '/user-message-list';
      const messages = await get(url);
      $('#read-msg').addClass('dashboard__highlight-item');
      $('#chat__dynamic').empty();
      messages.forEach(({ sender, message }) => {
      const msgList = `<li id="chat_${sender.id}" class="chat-list">
        <a href="#">
          <div class="chat-list-image online">
                <img src="/static/images/profile_photo_placeholder.jpeg" alt="Profile Photo" class="dashboard__user-avatar">
              </div>

              <div class="chat-details">
                <h4 id="name" class="name">${sender.username}</h4>
                <p class="accept__reject-btns">
                 ${message.text}
                 </p>
               </div>

               <div class="content">
                 <h6 class="content-timestamp">${message.created_at}</h6>
               </div>
             </a>
           </li>
          `
        $('#chat__dynamic').append(msgList);
      });
    } catch(err) {
      console.log(err);
    }
  }
  messageList(); 
  $('#dashboard__main-dynamic').on('click', '#read-msg', function() {
    messageList();
  });
});
