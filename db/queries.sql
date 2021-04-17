-- :name create_table_package
create table if not exists package (
    tracking_number     text    not null primary key,
    package_name        text,
    in_progress         integer not null default 1,
    last_checked        text,
    added               text    not null default current_timestamp
)

-- :name create_table_package_event
create table if not exists package_event (
    event_id            integer not null primary key,
    tracking_number     text    not null,
    event_datetime      text    not null,
    event_description   text    not null,
    is_delivery_event   integer not null default 0,
    added               text    not null default current_timestamp
)

-- :name create_table_package_subscription
create table if not exists package_subscription (
    tracking_number     text    not null,
    subscriber_id       text    not null,
    last_sent_event_id  integer not null default -1,
    added               text    not null default current_timestamp
)


-- :name get_package :one
select p.*
  from package p
 where p.tracking_number = :tracking_number

-- :name get_active_packages :many
select p.*
  from package p
 where p.in_progress = 1
 order by p.last_checked asc

-- :name insert_package :insert
insert into package (
    tracking_number,
    package_name)
values (
    :tracking_number,
    :package_name)

-- :name update_package_progress :affected
update package p
   set p.in_progress = :in_progress,
       p.last_checked = :last_checked
 where p.tracking_number = :tracking_number


-- :name get_events :many
select e.*
  from package_event e
 where e.tracking_number = :tracking_number
order by e.event_id desc

-- :name insert_event :insert
insert into package_event (    
    tracking_number,
    event_datetime,
    event_description,
    is_delivery_event)
values (
    :tracking_number,
    :event_datetime,
    :event_description,
    :is_delivery_event)


-- :name get_package_subscribers :many
select s.*
  from package_subscription s
 where s.tracking_number = :tracking_number
 order by s.added asc

-- :name get_subscriber_packages :many
select s.*
  from package_subscription s
 where s.subscriber_id = :subscriber_id
 order by s.added asc

-- :name subscribe :insert
insert into package_subscription (
    tracking_number,
    subscriber_id)
values (
    :tracking_number,
    :subscriber_id)

-- :name unsubscribe :affected
delete from package_subscription s
 where s.tracking_number = :tracking_number
   and s.subscriber_id   = :subscriber_id
