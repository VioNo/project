-- Создание последовательности для users
CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Создание таблицы users
CREATE TABLE public.users (
    id integer DEFAULT nextval('public.users_id_seq'::regclass) NOT NULL,
    login character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL
);

-- Создание таблицы tasks (с автоинкрементом через IDENTITY)
CREATE TABLE public.tasks (
    id integer GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    status character varying(50) NOT NULL,
    user_id integer NOT NULL,
    create_at date DEFAULT CURRENT_DATE NOT NULL
);

-- Установка текущего значения последовательности для users
SELECT pg_catalog.setval('public.users_id_seq', 61, true);

-- Добавление ограничений для users
ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

-- Добавление ограничений для tasks
ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);

-- Добавление внешнего ключа для связи tasks с users
ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;