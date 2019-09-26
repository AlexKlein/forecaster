create table fc_api_logs (updated_at       timestamp,
                          author_login     varchar(256),
                          url              varchar(1024),
                          parameters_dict  varchar(1024),
                          jsondata         text);

comment on table fc_api_logs is 'API response logging';

comment on column fc_api_logs.updated_at      is 'Record Update Date / Time';
comment on column fc_api_logs.author_login    is 'Change Author';
comment on column fc_api_logs.url             is 'API URL';
comment on column fc_api_logs.parameters_dict is 'Parameters with which the query was launched';
comment on column fc_api_logs.jsondata        is 'API response';

create table fc_daily_weather (value_day   date,
                               country     varchar(256),
                               city        varchar(256),
                               description varchar(256),
                               temp        float,
                               pressure    float,
                               humidity    float,
                               temp_min    float,
                               temp_max    float,
                               source      varchar(256));

comment on table fc_daily_weather is 'Daily weather forecast in cities';

comment on column fc_daily_weather.value_day   is 'Measurement day';
comment on column fc_daily_weather.country     is 'Country';
comment on column fc_daily_weather.city        is 'City';
comment on column fc_daily_weather.description is 'Weather description';
comment on column fc_daily_weather.temp        is 'Average temperature';
comment on column fc_daily_weather.pressure    is 'Atmosphere pressure';
comment on column fc_daily_weather.humidity    is 'Air humidity';
comment on column fc_daily_weather.temp_min    is 'Minimum daily temperature';
comment on column fc_daily_weather.temp_max    is 'Maximum daily temperature';
comment on column fc_daily_weather.source      is 'Source system of data receiving';

create table fc_weekly_weather (value_day   date,
                                country     varchar(256),
                                city        varchar(256),
                                temp        float,
                                pressure    float,
                                humidity    float,
                                source      varchar(256));

comment on table fc_weekly_weather is 'Monthly weather forecast in cities';

comment on column fc_weekly_weather.value_day   is 'Measurement day';
comment on column fc_weekly_weather.country     is 'Country';
comment on column fc_weekly_weather.city        is 'City';
comment on column fc_weekly_weather.temp        is 'Average temperature';
comment on column fc_weekly_weather.pressure    is 'Atmosphere pressure';
comment on column fc_weekly_weather.humidity    is 'Air humidity';
comment on column fc_weekly_weather.source      is 'Source system of data receiving';

create table fc_user_roles (user_role varchar(256),
                            user_name varchar(256));

comment on table fc_user_roles is 'List of users and roles with access to the application';

comment on column fc_user_roles.user_role is 'User role';
comment on column fc_user_roles.user_name is 'User Login';

create unique index fc_user_roles_pk on fc_user_roles
(user_name, user_role);

create table fc_api_task_queue (task_id     varchar(256),
                                 user_name   varchar(64),
                                 method      varchar(64),
                                 task_status varchar(16));

comment on table fc_api_task_queue is 'API task queue';

comment on column fc_api_task_queue.task_id     is 'Unique task key';
comment on column fc_api_task_queue.user_name   is 'User Login';
comment on column fc_api_task_queue.method      is 'Launched Application Method';
comment on column fc_api_task_queue.task_status is 'Task status';

create unique index fc_api_task_queue_pk on fc_api_task_queue
(task_id);