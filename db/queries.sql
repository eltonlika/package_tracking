-- :name create_table_package
create table if not exists package (
    tracking_number     text    not null primary key,
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
    added               text    not null default current_timestamp,
    unique (tracking_number, event_id)
)

-- :name create_table_package_subscription
create table if not exists package_subscription (
    tracking_number     text    not null,
    subscriber_id       text    not null,
    last_sent_event_id  integer not null default -1,
    package_name        text,
    added               text    not null default current_timestamp,
    primary key (tracking_number, subscriber_id)
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
insert into package (tracking_number) values (:tracking_number)

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
    subscriber_id,
    package_name)
values (
    :tracking_number,
    :subscriber_id,
    :package_name)

-- :name unsubscribe :affected
delete from package_subscription s
 where s.tracking_number = :tracking_number
   and s.subscriber_id   = :subscriber_id

-- :name update_subscriber_notified :affected
update package_subscription p
   set p.last_sent_event_id = :last_sent_event_id
 where p.tracking_number = :tracking_number
   and p.subscriber_id = :subscriber_id


-- :name get_events_to_notify :many
select s.subscriber_id,
       s.package_name,
       e.event_datetime,
       e.event_description
  from package_subscription s, package_event e
 where s.tracking_number = e.tracking_number
   and e.event_id > s.last_sent_event_id
  order by s.tracking_number asc, s.subscriber_id asc, e.event_id desc
  limit 30