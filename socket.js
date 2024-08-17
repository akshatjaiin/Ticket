function addMessage(message) {
    const messageList = $('#message-list-div')[0];

    // Any updates here should also be done to messages/detail.html
    messageList.innerHTML += `
          div id="message-${message.id}" class="w-full px-5 py-1 justify-center flex flex-row gap-3.5 relative"
            a id="message-${message.ID}-user-icon" class="cursor-pointer user-icon-popup-link"
              <img class="size-10 flex-none aspect-square object-cover rounded-full mt-1"
                   src="${message.author.display_avatar}" alt="${message.author.username}">
              div class="hidden user-icon-popup" id="message-${message.id}-profile"
                {% include 'users/profile.html' with user=message.author %}
              /div
            /a
            div id="message-${message.id}-child" class="grow text-gray-300 flex flex-col"
              h4 class="text-lg font-bold"${message.author.username}/h4
              p${message.content}/p

              ${message.attachments.length > 0 ? `
                div id="message-${message.id}-attachments" class="flex flex-row gap-3.5"
                  ${message.attachments.map((attachment) => `
                    a href="${attachment.download_url}" target="_blank" class="inline-block min-w-20 py-1 px-2.5 rounded-xl bg-gray-700 text-white cursor-pointer"${attachment.name}/a
                  `).join('')}
                /div
              ` : ''}
            /div
          /div
        `