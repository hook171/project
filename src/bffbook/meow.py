{% extends 'base.html' %}

{% block title %}
posts
{% endblock title %}

{% block content %}

<div class="ui grid">
        <div class="eleven wide column">
            {% for obj in qs %}

                <div class="ui fluid card">
                    <div class="content">
                        <div class="right floated meta">
                            <div class="ui grid">
                                 <div class="row">
                                    {% if request.user == obj.author.user %}
                                         <a href=""><button class="ui button bwhite-lg">Изменить</button></a>
                                         <a href=""><button class="ui button bwhite-lg">Удалить</button></a>
                                     {% endif %}
                                 </div>
                            </div>
                        </div>
                            <img class="ui avatar image" src={{obj.author.avatar.url}}>
                            {{ obj.author.user }} - {{ obj.created|timesince}} ago
                    </div>
                    <div class="ui fluid image">
                        {% if obj.image %}
                            <img src={{obj.image.url}}>
                        {% endif %}
                    </div>


                    <div class="content">
                        <p>{{obj.content}}</p>
                        <div class="right floated">
                            <form action="{% url 'posts:like-post-view' %}" method = "POST">
                                {% csrf_token %}

                            <input type="hidden" name="post_id" value={{obj.id}}>
                                {% if profile not in obj.liked.all %}
                                    <button type="submit" class="ui bwhite-sm button"></button>
                                    <span>{{obj.num_likes}} Likes </span>
                                {% else %}
                                    <button type="submit" class="ui bwhite-sm button"></button>
                                    <span>{{obj.num_likes}} Likes </span>
                                {% endif %}
                            </form>
                        </div>
                        <i class="comment icon"></i>
                        <span>{{ obj.num_comments }} comments</span>
                    </div>
                    <div class="extra content">
                        <div class="mb-5">

                        </div>
                        <button class="cmt_btn ui button mb-5">Показать/Скрыть комментарии</button>
                        <div class="comment-box">
                            {% if obj.comment_set.all %}
                                {% for c in obj.comment_set.all %}
                                    <div class="ui segment mb-5">
                                        <img class="ui avatar image" src={{c.user.avatar.url}}>
                                        <span>{{c.user}}</span>
                                        <div class="mt-5">{{c.body}}</div>
                                    </div>
                                {% endfor %}
                            {% endif %}
                        </div>

                        <form action = "" method="POST" class = "ui fluid form">
                            {%csrf_token%}
                            <input type="hidden" name="post_id" value={{obj.id}}>
                            {{c_form}}
                            <button type="sumbit" class="ui primary button mt-5 w-full" name="sumbit_c_form"> Прокомментировать </button>
                        </form>

                    </div>
                </div>
            {% endfor %}

        </div>


        <div class="five wide column">
            {% if post_added %}
                <div class="ui green message">Запись создана</div>
            {% endif %}
            <form action="" method="POST" class='ui form' enctype="multipart/form-data">
                {% csrf_token %}
                {{p_form}}
                <button type='submit' class="ui button positive" name="sumbit_p_form">Создать пост</button>
            </form>
        </div>
</div>
{% endblock content %}



{% block scripts %}
    <script>
        $( document ).ready(function() {
            let display = false
            $(".cmt_btn").click(function () {
                if (display===false) {
                    $(this).next(".comment-box").show("slow");
                    display=true
                } else {
                    $(this).next(".comment-box").hide("slow");
                    display=false
                }
            });

            $('.like-form').submit(function(e){
                e.preventDefault()

                const post_id = $(this).attr('id')

                const likeText = $(`.like-btn${post_id}`).text()
                const trim = $.trim(likeText)

                const url = $(this).attr('action')

                let res;
                const likes = $(`.like-count${post_id}`).text()
                const trimCount = parseInt(likes)

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        'post_id':post_id,
                    },
                    success: function(response) {
                        if(trim === 'Unlike') {
                            $(`.like-btn${post_id}`).text('Like')
                            res = trimCount - 1
                        } else {
                            $(`.like-btn${post_id}`).text('Unlike')
                            res = trimCount + 1
                        }

                        $(`.like-count${post_id}`).text(res)
                    },
                    error: function(response) {
                        console.log('error', response)
                    }
                })

            })
        });
    </script>
{% endblock scripts %}