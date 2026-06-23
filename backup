--
-- PostgreSQL database cluster dump
--

-- Started on 2026-06-23 21:09:56

\restrict 49lqpJlmIZgkggovTNFZvdPqaRGyIiKcaThu7iE6HHKY1XH3kiQMCvYMweVjx3M

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:4t5R+KTj7C55UoqDVrtPgg==$LCOVjvE/udEDX8b89tGH2OAecKFS+xlbX1u5TJes9jI=:tA2k55tjEd8/1zZ4L1tHA1CF3g2rN2ToJxcrh8/bELQ=';

--
-- User Configurations
--








\unrestrict 49lqpJlmIZgkggovTNFZvdPqaRGyIiKcaThu7iE6HHKY1XH3kiQMCvYMweVjx3M

--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

\restrict 71DOOhWNiZz7oh3rtbhRSYKP9Bzxjw1WL7NJphnTB82Tx0TUtwuzq56pDYm62cr

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-06-23 21:09:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2026-06-23 21:09:56

--
-- PostgreSQL database dump complete
--

\unrestrict 71DOOhWNiZz7oh3rtbhRSYKP9Bzxjw1WL7NJphnTB82Tx0TUtwuzq56pDYm62cr

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

\restrict vpIAgPnahwrWWkNxfzFhxOJ6cnV84pzYlWFZQwhKdpMqVclHODkHkvEV0nTmygp

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

-- Started on 2026-06-23 21:09:56

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 254 (class 1259 OID 49378)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    user_id integer NOT NULL,
    role character varying(50) DEFAULT 'moderator'::character varying,
    added_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 49377)
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO postgres;

--
-- TOC entry 5153 (class 0 OID 0)
-- Dependencies: 253
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- TOC entry 236 (class 1259 OID 32929)
-- Name: ai_learning_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_learning_analysis (
    id integer NOT NULL,
    test_id integer,
    user_id integer,
    analysis_text text NOT NULL,
    generated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    analysis_questions text
);


ALTER TABLE public.ai_learning_analysis OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 32928)
-- Name: ai_learning_analysis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_learning_analysis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_learning_analysis_id_seq OWNER TO postgres;

--
-- TOC entry 5154 (class 0 OID 0)
-- Dependencies: 235
-- Name: ai_learning_analysis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_learning_analysis_id_seq OWNED BY public.ai_learning_analysis.id;


--
-- TOC entry 220 (class 1259 OID 16423)
-- Name: promo_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promo_codes (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    discount_percent integer DEFAULT 0,
    max_uses integer DEFAULT 1,
    used_count integer DEFAULT 0,
    is_active boolean DEFAULT true,
    expires_at timestamp without time zone
);


ALTER TABLE public.promo_codes OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16422)
-- Name: promo_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.promo_codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.promo_codes_id_seq OWNER TO postgres;

--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 219
-- Name: promo_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.promo_codes_id_seq OWNED BY public.promo_codes.id;


--
-- TOC entry 228 (class 1259 OID 16501)
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    test_id integer,
    question_text text NOT NULL,
    option_a text NOT NULL,
    option_b text NOT NULL,
    option_c text NOT NULL,
    option_d text NOT NULL,
    correct_answer character(1) NOT NULL
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16500)
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questions_id_seq OWNER TO postgres;

--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 227
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- TOC entry 222 (class 1259 OID 16437)
-- Name: referrals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.referrals (
    id integer NOT NULL,
    user_id integer NOT NULL,
    by_user_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    bonus_amount integer DEFAULT 0
);


ALTER TABLE public.referrals OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16436)
-- Name: referrals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.referrals_id_seq OWNER TO postgres;

--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 221
-- Name: referrals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.referrals_id_seq OWNED BY public.referrals.id;


--
-- TOC entry 252 (class 1259 OID 41258)
-- Name: scoin_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scoin_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount integer NOT NULL,
    description character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scoin_history OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 41257)
-- Name: scoin_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.scoin_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scoin_history_id_seq OWNER TO postgres;

--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 251
-- Name: scoin_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.scoin_history_id_seq OWNED BY public.scoin_history.id;


--
-- TOC entry 244 (class 1259 OID 41208)
-- Name: shop_animations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_animations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    price integer DEFAULT 0 NOT NULL,
    css_code text,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.shop_animations OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 41207)
-- Name: shop_animations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_animations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_animations_id_seq OWNER TO postgres;

--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 243
-- Name: shop_animations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_animations_id_seq OWNED BY public.shop_animations.id;


--
-- TOC entry 248 (class 1259 OID 41230)
-- Name: shop_backgrounds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_backgrounds (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    price integer DEFAULT 0 NOT NULL,
    picture character varying(255),
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.shop_backgrounds OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 41229)
-- Name: shop_backgrounds_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_backgrounds_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_backgrounds_id_seq OWNER TO postgres;

--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 247
-- Name: shop_backgrounds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_backgrounds_id_seq OWNED BY public.shop_backgrounds.id;


--
-- TOC entry 246 (class 1259 OID 41219)
-- Name: shop_colors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_colors (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    price integer DEFAULT 0 NOT NULL,
    color character varying(255),
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.shop_colors OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 41218)
-- Name: shop_colors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_colors_id_seq OWNER TO postgres;

--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 245
-- Name: shop_colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_colors_id_seq OWNED BY public.shop_colors.id;


--
-- TOC entry 250 (class 1259 OID 41241)
-- Name: shop_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    item_type character varying(50) NOT NULL,
    item_id integer NOT NULL,
    item_name character varying(255) NOT NULL,
    price integer NOT NULL,
    details text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.shop_history OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 41240)
-- Name: shop_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_history_id_seq OWNER TO postgres;

--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 249
-- Name: shop_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_history_id_seq OWNED BY public.shop_history.id;


--
-- TOC entry 242 (class 1259 OID 41197)
-- Name: shop_ranks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shop_ranks (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    price integer DEFAULT 0 NOT NULL,
    picture character varying(255),
    name_color character varying(20),
    rank_color character varying(20),
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.shop_ranks OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 41196)
-- Name: shop_ranks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shop_ranks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shop_ranks_id_seq OWNER TO postgres;

--
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 241
-- Name: shop_ranks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shop_ranks_id_seq OWNED BY public.shop_ranks.id;


--
-- TOC entry 234 (class 1259 OID 32893)
-- Name: telegram_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.telegram_accounts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tg_id character varying(55) NOT NULL,
    username character varying(255),
    first_name character varying(255) NOT NULL,
    last_name character varying(255),
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.telegram_accounts OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 32892)
-- Name: telegram_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.telegram_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.telegram_accounts_id_seq OWNER TO postgres;

--
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 233
-- Name: telegram_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.telegram_accounts_id_seq OWNED BY public.telegram_accounts.id;


--
-- TOC entry 238 (class 1259 OID 32969)
-- Name: test_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_results (
    id integer NOT NULL,
    user_id integer NOT NULL,
    test_id integer NOT NULL,
    correct_answers integer NOT NULL,
    total_questions integer NOT NULL,
    percentage double precision NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.test_results OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 32968)
-- Name: test_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_results_id_seq OWNER TO postgres;

--
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 237
-- Name: test_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_results_id_seq OWNED BY public.test_results.id;


--
-- TOC entry 226 (class 1259 OID 16488)
-- Name: tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tests (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_id integer,
    description text,
    is_public boolean DEFAULT true,
    status text
);


ALTER TABLE public.tests OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16487)
-- Name: tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tests_id_seq OWNER TO postgres;

--
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 225
-- Name: tests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tests_id_seq OWNED BY public.tests.id;


--
-- TOC entry 230 (class 1259 OID 32863)
-- Name: user_allowed_tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_allowed_tests (
    id integer NOT NULL,
    user_id integer NOT NULL,
    test_id integer NOT NULL,
    allowed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_allowed_tests OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 32862)
-- Name: user_allowed_tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_allowed_tests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_allowed_tests_id_seq OWNER TO postgres;

--
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_allowed_tests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_allowed_tests_id_seq OWNED BY public.user_allowed_tests.id;


--
-- TOC entry 232 (class 1259 OID 32872)
-- Name: user_options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_options (
    id integer NOT NULL,
    test_id integer NOT NULL,
    user_id integer NOT NULL,
    options character varying DEFAULT '[]'::character varying,
    "end" boolean DEFAULT false
);


ALTER TABLE public.user_options OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 32871)
-- Name: user_options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_options_id_seq OWNER TO postgres;

--
-- TOC entry 5168 (class 0 OID 0)
-- Dependencies: 231
-- Name: user_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_options_id_seq OWNED BY public.user_options.id;


--
-- TOC entry 240 (class 1259 OID 41181)
-- Name: user_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_statuses (
    id integer NOT NULL,
    user_id integer NOT NULL,
    rank character varying(100) NOT NULL,
    picture character varying(255),
    animation text,
    color character varying(50),
    name_color character varying(20),
    rank_color character varying(20),
    css_code text
);


ALTER TABLE public.user_statuses OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 41180)
-- Name: user_statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_statuses_id_seq OWNER TO postgres;

--
-- TOC entry 5169 (class 0 OID 0)
-- Dependencies: 239
-- Name: user_statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_statuses_id_seq OWNED BY public.user_statuses.id;


--
-- TOC entry 224 (class 1259 OID 16458)
-- Name: user_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_tokens (
    id integer NOT NULL,
    token character varying(255) NOT NULL,
    user_id integer NOT NULL,
    ip_address character varying(45),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_tokens OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16457)
-- Name: user_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_tokens_id_seq OWNER TO postgres;

--
-- TOC entry 5170 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_tokens_id_seq OWNED BY public.user_tokens.id;


--
-- TOC entry 218 (class 1259 OID 16388)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password text NOT NULL,
    language character varying(5) DEFAULT 'uz'::character varying,
    theme character varying(10) DEFAULT 'light'::character varying,
    scoin integer DEFAULT 0 NOT NULL,
    xp integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    background text DEFAULT '/static/images/default_bg.png'::text,
    promo character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16387)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5171 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4882 (class 2604 OID 49381)
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- TOC entry 4861 (class 2604 OID 32932)
-- Name: ai_learning_analysis id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_learning_analysis ALTER COLUMN id SET DEFAULT nextval('public.ai_learning_analysis_id_seq'::regclass);


--
-- TOC entry 4839 (class 2604 OID 16426)
-- Name: promo_codes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promo_codes ALTER COLUMN id SET DEFAULT nextval('public.promo_codes_id_seq'::regclass);


--
-- TOC entry 4852 (class 2604 OID 16504)
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- TOC entry 4844 (class 2604 OID 16440)
-- Name: referrals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.referrals ALTER COLUMN id SET DEFAULT nextval('public.referrals_id_seq'::regclass);


--
-- TOC entry 4880 (class 2604 OID 41261)
-- Name: scoin_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scoin_history ALTER COLUMN id SET DEFAULT nextval('public.scoin_history_id_seq'::regclass);


--
-- TOC entry 4869 (class 2604 OID 41211)
-- Name: shop_animations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_animations ALTER COLUMN id SET DEFAULT nextval('public.shop_animations_id_seq'::regclass);


--
-- TOC entry 4875 (class 2604 OID 41233)
-- Name: shop_backgrounds id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_backgrounds ALTER COLUMN id SET DEFAULT nextval('public.shop_backgrounds_id_seq'::regclass);


--
-- TOC entry 4872 (class 2604 OID 41222)
-- Name: shop_colors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_colors ALTER COLUMN id SET DEFAULT nextval('public.shop_colors_id_seq'::regclass);


--
-- TOC entry 4878 (class 2604 OID 41244)
-- Name: shop_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_history ALTER COLUMN id SET DEFAULT nextval('public.shop_history_id_seq'::regclass);


--
-- TOC entry 4866 (class 2604 OID 41200)
-- Name: shop_ranks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_ranks ALTER COLUMN id SET DEFAULT nextval('public.shop_ranks_id_seq'::regclass);


--
-- TOC entry 4858 (class 2604 OID 32896)
-- Name: telegram_accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telegram_accounts ALTER COLUMN id SET DEFAULT nextval('public.telegram_accounts_id_seq'::regclass);


--
-- TOC entry 4863 (class 2604 OID 32972)
-- Name: test_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_results ALTER COLUMN id SET DEFAULT nextval('public.test_results_id_seq'::regclass);


--
-- TOC entry 4849 (class 2604 OID 16491)
-- Name: tests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests ALTER COLUMN id SET DEFAULT nextval('public.tests_id_seq'::regclass);


--
-- TOC entry 4853 (class 2604 OID 32866)
-- Name: user_allowed_tests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_allowed_tests ALTER COLUMN id SET DEFAULT nextval('public.user_allowed_tests_id_seq'::regclass);


--
-- TOC entry 4855 (class 2604 OID 32875)
-- Name: user_options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_options ALTER COLUMN id SET DEFAULT nextval('public.user_options_id_seq'::regclass);


--
-- TOC entry 4865 (class 2604 OID 41184)
-- Name: user_statuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_statuses ALTER COLUMN id SET DEFAULT nextval('public.user_statuses_id_seq'::regclass);


--
-- TOC entry 4847 (class 2604 OID 16461)
-- Name: user_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tokens ALTER COLUMN id SET DEFAULT nextval('public.user_tokens_id_seq'::regclass);


--
-- TOC entry 4832 (class 2604 OID 16391)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5147 (class 0 OID 49378)
-- Dependencies: 254
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, user_id, role, added_at) FROM stdin;
1	6	moderator	2026-06-17 09:55:53.218188+05
3	14	moderator	2026-06-21 19:16:06.084943+05
\.


--
-- TOC entry 5129 (class 0 OID 32929)
-- Dependencies: 236
-- Data for Name: ai_learning_analysis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_learning_analysis (id, test_id, user_id, analysis_text, generated_at, analysis_questions) FROM stdin;
24	\N	\N	Assalomu alaykum! Tajribali metodist sifatida taqdim etilgan geometrik test savollarini tahlil qildim. Quyida ushbu testning pedagogik tahlili va har bir savolning yechimi keltirilgan.\n\n---\n\n### 📊 Testning pedagogik tahlili\n\n**1. Mavzular qamrovi:**\nTest geometriya fanining "Yuzalar" va "Perimetr" mavzularini qamrab olgan. Savollar murakkab shakllarni oddiy geometrik shakllarga ajratib hisoblash (yig'indi va ayirma usuli) ko'nikmasini tekshirishga qaratilgan.\n\n**2. Murakkablik darajasi:**\nSavollar o'rta maktab o'quvchilari uchun moslashtirilgan. Ular o'quvchidan nafaqat formulani bilishni, balki fazoviy tasavvur va mantiqiy fikrlashni talab qiladi.\n\n**3. Sifat va variantlar tahlili:**\n*   **Ijobiy tomoni:** Variantlar o'quvchilar ko'p yo'l qo'yadigan xatolarni (masalan, formuladagi koeffitsiyentlarni unutish yoki noto'g'ri arifmetik amallar) hisobga olgan holda tuzilgan.\n*   **Tavsiya:** 3-savolda $\\pi=3$ deb olinishi aniq ko'rsatilgani juda yaxshi, bu hisoblashdagi chalkashliklarning oldini oladi. 4-savolda "L" shaklidagi poligonning barcha tomonlari berilgani o'quvchi uchun qulaylik yaratadi.\n\n---\n\n### 📝 Savollarning yechimi va tahlili\n\n| Savol № | Yechim jarayoni | To'g'ri javob |\n| :--- | :--- | :--- |\n| **1** | To'g'ri to'rtburchak yuzi: $8 \\times 5 = 40$. Uchburchak yuzi: $(8 \\times 3) / 2 = 12$. Umumiy yuzi: $40 + 12 = 52$. | **B** |\n| **2** | Katta kvadrat yuzi: $6^2 = 36$. Kichik kvadrat yuzi: $2^2 = 4$. Qolgan yuz: $36 - 4 = 32$. | **A** |\n| **3** | Kvadrat yuzi: $8^2 = 64$. Doira yuzi: $\\pi \\times r^2 = 3 \\times 4^2 = 3 \\times 16 = 48$. Qolgan yuz: $64 - 48 = 16$. | **A** |\n| **4** | Perimetr barcha tashqi tomonlar yig'indisi: $10 + 4 + 6 + 2 + 4 + 6 = 32$. | **C** |\n| **5** | Trapetsiya yuzi formulasi: $S = \\frac{a+b}{2} \\times h = \\frac{10+6}{2} \\times 4 = 8 \\times 4 = 32$. | **A** |\n\n---\n\n### 💡 Xulosa\nTest savollari o'zining mantiqiy ketma-ketligi va qiyinchilik darajasi bo'yicha **yuqori sifatli** deb baholanadi. Ular o'quvchining geometrik shakllar bilan ishlash malakasini aniq o'lchab bera oladi. \n\n**Metodist maslahati:** Agar ushbu test imtihon uchun ishlatilsa, 4-savolda "L" shaklidagi poligonning chizmasini vizual tarzda ilova qilish o'quvchilar uchun tushunishni yanada osonlashtiradi.	2026-06-11 18:08:28.672967+05	[{"id": 456, "question": "Shakl 1: To'g'ri to'rtburchak (a=8, b=5) va unga yopishgan uchburchak (asos=8, balandlik=3) berilgan. Shaklning umumiy yuzini toping.", "options": {"A": "40", "B": "52", "C": "48", "D": "56"}, "correct": "B", "image_path": null}, {"id": 457, "question": "Shakl 2: Tomoni a=6 bo'lgan kvadrat va uning ichidan kesib olingan tomoni a=2 bo'lgan kichik kvadrat qolgan yuzani toping.", "options": {"A": "32", "B": "36", "C": "28", "D": "30"}, "correct": "A", "image_path": null}, {"id": 458, "question": "Shakl 3: Tomoni a=8 bo'lgan kvadrat ichida joylashgan radiusi r=4 bo'lgan doira yuzasini kvadrat yuzasidan ayirib, qolgan qismning yuzasini toping (pi=3 deb olinsin).", "options": {"A": "16", "B": "24", "C": "32", "D": "48"}, "correct": "A", "image_path": null}, {"id": 459, "question": "Shakl 4: \\"L\\" shaklidagi poligonning tomonlari (10, 4, 6, 2, 4, 6) berilgan. Ushbu shaklning perimetrini hisoblang.", "options": {"A": "28", "B": "30", "C": "32", "D": "36"}, "correct": "C", "image_path": null}, {"id": 460, "question": "Shakl 5: Asoslari a=10, b=6 va balandligi h=4 bo'lgan trapetsiyaning yuzasini toping.", "options": {"A": "32", "B": "40", "C": "48", "D": "64"}, "correct": "A", "image_path": null}]
25	\N	\N	Assalomu alaykum. Tajribali metodist sifatida taqdim etilgan test savollarini tahlil qildim. Quyida ushbu test bo‘yicha pedagogik xulosa va savollarning tahlili keltirilgan.\n\n---\n\n### **Pedagogik Tahlil va Xulosa**\n\n**1. Mavzu qamrovi:**\nTest to‘liq **"Past Simple" (O‘tgan oddiy zamon)** mavzusiga bag‘ishlangan. Unda fe’llarning o‘tgan zamon shakllari (to‘g‘ri va noto‘g‘ri fe’llar), inkor va so‘roq gaplar hamda "to be" fe’lining o‘tgan zamon shakllari qamrab olingan.\n\n**2. Murakkablik darajasi:**\nTest boshlang‘ich va o‘rta darajadagi (A1-A2) o‘quvchilar uchun mo‘ljallangan. Savollar mantiqiy ketma-ketlikda tuzilgan bo‘lib, o‘quvchidan asosiy grammatik qoidalarni (yordamchi fe’l "did" ishlatilishi, noto‘g‘ri fe’llarning shakllari) bilishni talab qiladi.\n\n**3. Variantlarning sifati:**\n*   **Ijobiy tomoni:** Chalg‘ituvchi variantlar (distraktorlar) yaxshi tanlangan. Masalan, noto‘g‘ri fe’llarning noto‘g‘ri yasalgan shakllari (masalan, *sleeped, runned, buyed*) o‘quvchining qoidani qay darajada tushunganini tekshirish uchun juda samarali.\n*   **Tavsiya:** Testda faqat "Past Simple"ga urg‘u berilgan. Agar testni yanada boyitmoqchi bo‘lsangiz, kelajakda "Past Simple"ni "Present Simple" bilan solishtiruvchi savollarni ham qo‘shish maqsadga muvofiq bo‘ladi.\n\n**4. Umumiy xulosa:**\nTest o‘z maqsadiga to‘liq javob beradi. U o‘quvchining o‘tgan zamon qoidalarini amaliyotda qo‘llay olish qobiliyatini aniq o‘lchab bera oladi. Savollar aniq va tushunarli tuzilgan.\n\n---\n\n### **Savollar va To‘g‘ri Javoblar tahlili**\n\n| Savol № | To‘g‘ri javob | Izoh |\n| :--- | :---: | :--- |\n| 1 | **B** | *went* (go fe’lining II shakli) |\n| 2 | **A** | *didn't play* (inkor shakli) |\n| 3 | **C** | *Was* (he uchun o‘tgan zamon) |\n| 4 | **A** | *saw* (see fe’lining II shakli) |\n| 5 | **C** | *had* (have fe’lining II shakli) |\n| 6 | **B** | *did* (do fe’lining II shakli) |\n| 7 | **B** | *did you cry* (so‘roq gap) |\n| 8 | **A** | *didn't drink* (inkor shakli) |\n| 9 | **B** | *was* (it uchun o‘tgan zamon) |\n| 10 | **C** | *bought* (buy fe’lining II shakli) |\n| 11 | **B** | *wrote* (write fe’lining II shakli) |\n| 12 | **B** | *slept* (sleep fe’lining II shakli) |\n| 13 | **A** | *didn't listen* (inkor shakli) |\n| 14 | **B** | *Did she come* (so‘roq gap) |\n| 15 | **A** | *ate* (eat fe’lining II shakli) |\n| 16 | **C** | *ran* (run fe’lining II shakli) |\n| 17 | **B** | *Did they like* (so‘roq gap) |\n| 18 | **C** | *flew* (fly fe’lining II shakli) |\n| 19 | **B** | *found* (find fe’lining II shakli) |\n| 20 | **C** | *were* (they uchun o‘tgan zamon) |\n\nUshbu test o‘quvchilarni baholash uchun juda sifatli va metodik jihatdan to‘g‘ri shakllantirilgan.	2026-06-11 18:09:42.678698+05	[{"id": 461, "question": "She ____ (go) to the cinema yesterday.", "options": {"A": "go", "B": "went", "C": "goes", "D": "gone"}, "correct": "B", "image_path": null}, {"id": 462, "question": "They ____ (not / play) football last week.", "options": {"A": "didn't play", "B": "don't play", "C": "not played", "D": "doesn't play"}, "correct": "A", "image_path": null}, {"id": 463, "question": "____ (be) he at home?", "options": {"A": "Do", "B": "Did", "C": "Was", "D": "Were"}, "correct": "C", "image_path": null}, {"id": 464, "question": "I ____ (see) a ghost!", "options": {"A": "saw", "B": "see", "C": "seen", "D": "sees"}, "correct": "A", "image_path": null}, {"id": 465, "question": "We ____ (have) a big house.", "options": {"A": "has", "B": "have", "C": "had", "D": "having"}, "correct": "C", "image_path": null}, {"id": 466, "question": "He ____ (do) his homework.", "options": {"A": "does", "B": "did", "C": "doing", "D": "done"}, "correct": "B", "image_path": null}, {"id": 467, "question": "Why ____ (you / cry)?", "options": {"A": "do you cry", "B": "did you cry", "C": "you cried", "D": "were you cry"}, "correct": "B", "image_path": null}, {"id": 468, "question": "She ____ (not / drink) tea.", "options": {"A": "didn't drink", "B": "doesn't drink", "C": "not drank", "D": "don't drink"}, "correct": "A", "image_path": null}, {"id": 469, "question": "It ____ (be) a sunny day.", "options": {"A": "is", "B": "was", "C": "were", "D": "been"}, "correct": "B", "image_path": null}, {"id": 470, "question": "They ____ (buy) a new car.", "options": {"A": "buyed", "B": "buys", "C": "bought", "D": "buying"}, "correct": "C", "image_path": null}, {"id": 471, "question": "Who ____ (write) this?", "options": {"A": "writed", "B": "wrote", "C": "writes", "D": "writing"}, "correct": "B", "image_path": null}, {"id": 472, "question": "I ____ (sleep) 10 hours.", "options": {"A": "sleeped", "B": "slept", "C": "sleep", "D": "slapt"}, "correct": "B", "image_path": null}, {"id": 473, "question": "You ____ (not / listen).", "options": {"A": "didn't listen", "B": "don't listen", "C": "not listened", "D": "doesn't listen"}, "correct": "A", "image_path": null}, {"id": 474, "question": "____ (she / come) late?", "options": {"A": "Does she come", "B": "Did she come", "C": "Was she come", "D": "Did she came"}, "correct": "B", "image_path": null}, {"id": 475, "question": "We ____ (eat) pizza.", "options": {"A": "ate", "B": "eated", "C": "eats", "D": "eating"}, "correct": "A", "image_path": null}, {"id": 476, "question": "The cat ____ (run) fast.", "options": {"A": "run", "B": "runs", "C": "ran", "D": "runned"}, "correct": "C", "image_path": null}, {"id": 477, "question": "____ (they / like) it?", "options": {"A": "Do they like", "B": "Did they like", "C": "Were they like", "D": "Did they liked"}, "correct": "B", "image_path": null}, {"id": 478, "question": "He ____ (fly) to London.", "options": {"A": "flied", "B": "flyed", "C": "flew", "D": "flies"}, "correct": "C", "image_path": null}, {"id": 479, "question": "I ____ (find) my keys.", "options": {"A": "finded", "B": "found", "C": "find", "D": "fined"}, "correct": "B", "image_path": null}, {"id": 480, "question": "They ____ (be) happy.", "options": {"A": "was", "B": "are", "C": "were", "D": "is"}, "correct": "C", "image_path": null}]
13	\N	\N	Hurmatli hamkasb, taqdim etilgan test savollarini sinchkovlik bilan tahlil qilib chiqdim. Quyida ushbu testning pedagogik xulosasi va tahlili keltirilgan.\n\n---\n\n# Test Savollarining Pedagogik Tahlili\n\n## 1. Qamrab Olingan Mavzular\n\nUshbu test savollari asosan **oddiy kasrlar va aralash kasrlar ustida qo'shish va ayirish amallari** mavzusini qamrab olgan. Xususan, quyidagi kichik mavzular tekshirilgan:\n\n*   **Har xil maxrajli oddiy kasrlarni qo'shish va ayirish:** Testning dastlabki savollari (1-7-savollar) aynan shu ko'nikmani tekshirishga qaratilgan. Bu yerda o'quvchidan umumiy maxraj topish, kasrlarni umumiy maxrajga keltirish va keyin amallarni bajarish talab etiladi.\n*   **Aralash kasrlarni qo'shish va ayirish:** 8-10-savollar aralash kasrlar bilan ishlash qobiliyatini baholaydi. Bu yerda butun va kasr qismlarini alohida-alohida qo'shish/ayirish yoki aralash kasrlarni noto'g'ri kasrga aylantirib hisoblash usullari qo'llaniladi. Ayniqsa, ayirishda "qarz olish" holatlari (10-savol) o'quvchining tushunchasini chuqurroq tekshiradi.\n*   **Kasrlar ishtirokidagi matnli masalalar:** 11-15-savollar kasrlar ustidagi amallarni real hayotiy vaziyatlarda qo'llash qobiliyatini baholaydi. Bu masalalar o'quvchining matematik bilimlarni amaliyotda tatbiq etish, masalani tahlil qilish va yechish ko'nikmalarini rivojlantirishga xizmat qiladi.\n\n**Eslatma:** Testda oddiy kasrlarni ko'paytirish va bo'lish amallari mavjud emas. Agar "Oddiy kasrlar ustida amallar" mavzusi to'liq qamrab olinishi kerak bo'lsa, bu amallar ham kiritilishi maqsadga muvofiq bo'lar edi.\n\n## 2. Savollarning Murakkablik Darajasi\n\nTest savollarining murakkablik darajasi muvozanatlangan bo'lib, boshlang'ich, o'rta va biroz qiyinroq darajadagi savollarni o'z ichiga oladi:\n\n*   **Boshlang'ich daraja (Oson):** 1, 2, 3, 4-savollar. Bu savollar kasrlarni umumiy maxrajga keltirish va oddiy qo'shish/ayirish amallarini bajarish bo'yicha asosiy bilimlarni tekshiradi. Maxrajlar nisbatan kichik va umumiy maxrajni topish oson.\n*   **O'rta daraja:** 5, 6, 7, 8, 9, 11, 13, 14-savollar. Bu savollar biroz ko'proq hisoblashni, kattaroq umumiy maxrajlarni topishni (masalan, 7/8 - 2/5 da 40), uchta kasr ustida amal bajarishni (7-savol) yoki aralash kasrlar bilan ishlashni (8, 9-savollar) talab qiladi. Matnli masalalar ham (11, 13, 14-savollar) o'rta darajada bo'lib, to'g'ri amalni tanlash va hisoblashni talab etadi.\n*   **Qiyinroq daraja:** 10, 12, 15-savollar.\n    *   10-savol aralash kasrlarni ayirishda butun qismdan "qarz olish"ni talab qiladi, bu ko'plab o'quvchilar uchun qiyinchilik tug'dirishi mumkin.\n    *   12-savol ham aralash kasrli matnli masala bo'lib, unda "qarz olish" holati mavjud.\n    *   15-savol esa ko'p bosqichli matnli masala bo'lib, avval ikkinchi tomonni topish, so'ngra perimetrni hisoblashni talab etadi. Bu o'quvchining mantiqiy fikrlash va ketma-ket amallarni bajarish qobiliyatini tekshiradi.\n\nUmuman olganda, murakkablik darajasi o'quvchilarning turli darajadagi bilim va ko'nikmalarini baholash imkonini beradi.\n\n## 3. Variantlarning Tanlanishi va Sifati\n\nVariantlar juda yaxshi tanlangan va testning diagnostik qiymatini oshiradi. Har bir savolda nafaqat to'g'ri javob, balki o'quvchilar tomonidan tez-tez qilinadigan tipik xatolar ham variantlar orasiga kiritilgan:\n\n*   **Maxrajlarni qo'shish/ayirish:** Masalan, 1-savolda A) 2/5 (surat va maxrajlarni to'g'ridan-to'g'ri qo'shish) yoki 5-savolda A) 3/7. Bu xato kasrlarni qo'shish/ayirishning asosiy qoidasini tushunmaslikdan kelib chiqadi.\n*   **Noto'g'ri umumiy maxraj topish yoki hisoblash xatolari:** Ko'plab savollarda shunday variantlar mavjud bo'lib, ular o'quvchining hisoblashdagi e'tiborsizligini yoki umumiy maxraj topishdagi kamchiliklarini aniqlashga yordam beradi.\n*   **Soddalashtirishni unutish:** 4-savolda D) 4/6 varianti to'g'ri javob B) 1/2 ning soddalashtirilmagan shakli. Bu o'quvchining javobni oxirigacha soddalashtirish ko'nikmasini tekshiradi.\n*   **Aralash kasrlarda xatolar:** 10-savolda A) 2 3/10 varianti "qarz olish"ni unutgan holda hisoblangan noto'g'ri javobdir. Bunday variantlar o'quvchining aralash kasrlar bilan ishlashdagi nozik jihatlarni qanchalik tushunganini ko'rsatadi.\n\nVariantlarning bunday puxta tanlanishi o'qituvchiga o'quvchilarning qaysi bosqichda xato qilayotganini aniqlashda katta yordam beradi.\n\n## 4. Testning Umumiy Sifati va Tavsiyalar\n\n**Ijobiy tomonlari:**\n\n*   **Aniqlik va tushunarlilik:** Savollar aniq va tushunarli qilib berilgan, hech qanday ikkilanishga o'rin qoldirmaydi.\n*   **Mavzuning yaxshi qamrab olinishi:** Oddiy va aralash kasrlarni qo'shish/ayirish bo'yicha barcha asosiy ko'nikmalar tekshirilgan.\n*   **Amaliy ahamiyat:** Matnli masalalar mavzuning amaliy ahamiyatini ko'rsatadi va o'quvchilarni real hayotiy vaziyatlarda matematik bilimlarni qo'llashga undaydi.\n*   **Diagnostik qiymat:** Variantlarning puxta tanlanishi testning diagnostik qiymatini oshiradi, ya'ni o'quvchilarning xato sabablarini aniqlashga yordam beradi.\n*   **Muvozanatlangan murakkablik:** Turli darajadagi savollar mavjudligi testni keng auditoriya uchun mos qiladi.\n\n**Kamchiliklar va takliflar:**\n\n*   **Rasmning maqsadsizligi:** 1-savolda berilgan rasm (img src="/static/uploads/quiz_images/a826da36-6977-4451-8403-0d48316e2af6.jpeg") savolning mazmuniga hech qanday qo'shimcha qiymat qo'shmaydi. Agar rasm qo'shiladigan bo'lsa, u kasrlarni vizualizatsiya qilishga (masalan, bo'yalgan qismlar orqali) yoki masalani tushunishga yordam berishi kerak. Hozirgi holatda u shunchaki "dekorativ" vazifasini o'tagan. Agar rasmning maqsadi bo'lmasa, uni olib tashlash yoki mazmunli rasm bilan almashtirish tavsiya etiladi.\n*   **Mavzu doirasini kengaytirish imkoniyati:** Yuqorida ta'kidlanganidek, agar "Oddiy kasrlar ustida amallar" mavzusi to'liq baholanishi kerak bo'lsa, kasrlarni ko'paytirish va bo'lish amallarini o'z ichiga olgan savollarni ham kiritish mumkin. Bu testning qamrovini yanada kengaytiradi.\n*   **Vaqt cheklovi:** Testning umumiy sifati yaxshi bo'lsa-da, bunday turdagi 15 ta savolni yechish uchun o'quvchilarga yetarli vaqt berilishi kerak, chunki ba'zi savollar (ayniqsa, matnli va aralash kasrli) ko'proq vaqt talab qiladi.\n\n**Xulosa:**\n\nUshbu test oddiy va aralash kasrlar ustida qo'shish va ayirish amallarini o'zlashtirish darajasini baholash uchun juda yaxshi vositadir. Savollarning murakkablik darajasi va variantlarning sifati yuqori bo'lib, o'quvchilarning bilim va ko'nikmalarini chuqur tahlil qilish imkonini beradi. Kichik kamchiliklar (rasmning maqsadsizligi, ko'paytirish/bo'lish amallarining yo'qligi) testning umumiy sifatiga jiddiy ta'sir qilmaydi, ammo kelajakda testlarni takomillashtirish uchun e'tiborga olish mumkin.	2026-06-06 10:39:44.458445+05	[{"id": 346, "question": "Hisoblang:  1/2 + 1/3 <br><img src=\\"/static/uploads/quiz_images/a826da36-6977-4451-8403-0d48316e2af6.jpeg\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "2/5", "B": "5/6", "C": "2/3", "D": "1/6"}, "correct": "B", "image_path": null}, {"id": 347, "question": "Hisoblang:  3/4 - 1/2", "options": {"A": "1/4", "B": "2/2", "C": "1/2", "D": "1/8"}, "correct": "A", "image_path": null}, {"id": 348, "question": "Amalni bajaring:  2/5 + 3/10", "options": {"A": "5/15", "B": "7/10", "C": "1/2", "D": "4/5"}, "correct": "B", "image_path": null}, {"id": 349, "question": "Hisoblang:  5/6 - 1/3", "options": {"A": "4/3", "B": "1/2", "C": "2/3", "D": "4/6"}, "correct": "B", "image_path": null}, {"id": 350, "question": "Yig‘indini toping:  2/3 + 1/4", "options": {"A": "3/7", "B": "11/12", "C": "7/12", "D": "5/12"}, "correct": "B", "image_path": null}, {"id": 351, "question": "Ayirmani hisoblang:  7/8 - 2/5", "options": {"A": "5/3", "B": "9/40", "C": "19/40", "D": "5/40"}, "correct": "C", "image_path": null}, {"id": 352, "question": "Hisoblang:  1 - 2/3 - 1/6", "options": {"A": "1/6", "B": "1/3", "C": "1/2", "D": "5/6"}, "correct": "A", "image_path": null}, {"id": 353, "question": "Hisoblang:  2 1/2 + 1 1/4", "options": {"A": "3 2/6", "B": "3 3/4", "C": "3 1/2", "D": "4 1/4"}, "correct": "B", "image_path": null}, {"id": 354, "question": "Ayirmani toping:  3 2/3 - 1 1/2", "options": {"A": "2 1/6", "B": "2 1/1", "C": "1 5/6", "D": "2 1/3"}, "correct": "A", "image_path": null}, {"id": 355, "question": "Hisoblang:  4 1/5 - 2 1/2", "options": {"A": "2 3/10", "B": "1 7/10", "C": "2 1/3", "D": "1 3/10"}, "correct": "B", "image_path": null}, {"id": 356, "question": "Madina do‘kondan 3/4 kg olma va 1/2 kg banan sotib oldi. U jami necha kilogramm meva sotib olgan?", "options": {"A": "1 1/4 kg", "B": "4/6 kg", "C": "1 1/2 kg", "D": "3/8 kg"}, "correct": "A", "image_path": null}, {"id": 357, "question": "Idishda 2 1/2 litr sut bor edi. Undan pirog pishirish uchun 3/4 litr sut ishlatildi. Idishda qancha sut qoldi?", "options": {"A": "1 1/2 litr", "B": "1 3/4 litr", "C": "2 1/4 litr", "D": "1 1/4 litr"}, "correct": "B", "image_path": null}, {"id": 358, "question": "Sayyoh birinchi soatda yo‘lning 1/3 qismini, ikkinchi soatda esa 2/5 qismini bosib o‘tdi. U ikki soatda yo‘lning qancha qismini bosib o‘tgan?", "options": {"A": "3/8 qismini", "B": "11/15 qismini", "C": "2/15 qismini", "D": "4/5 qismini"}, "correct": "B", "image_path": null}, {"id": 359, "question": "Hovuzdagi suvning 5/8 qismi to‘ldirilgan. Quyosh issig‘ida suvning 1/4 qismi bug‘lanib ketdi. Hovuzning qancha qismida suv qoldi?", "options": {"A": "4/4 qismi", "B": "1/2 qismi", "C": "3/8 qismi", "D": "1/8 qismi"}, "correct": "C", "image_path": null}, {"id": 360, "question": "Uchburchakning birinchi tomoni 1/2 m, ikkinchi tomoni birinchisidan 1/5 m uzun, uchinchi tomoni esa 3/10 m. Uchburchakning perimetrini toping.", "options": {"A": "1 1/2 m", "B": "1 m", "C": "1 2/5 m", "D": "9/10 m"}, "correct": "A", "image_path": null}]
14	\N	\N	# Test Savollari Tahlili: Kasrlar Ustida Amallar\n\nHurmatli hamkasblar, taqdim etilgan 15 ta test savolini chuqur pedagogik tahlil qilib chiqdim. Ushbu tahlil testning mavzular qamrovi, savollarning murakkablik darajasi, variantlarning sifati va testning umumiy samaradorligi haqida batafsil ma'lumot beradi.\n\n---\n\n## 1. Umumiy Ma'lumot\n\n*   **Testning maqsadi:** O'quvchilarning oddiy va aralash kasrlar ustida qo'shish va ayirish amallarini bajarish ko'nikmalarini baholash. Shuningdek, kasrlar bilan bog'liq matnli masalalarni yechish qobiliyatini tekshirish.\n*   **Mo'ljallangan sinf:** Odatda 5-6-sinf matematika kursiga mos keladi.\n*   **Savollar soni:** 15 ta.\n\n---\n\n## 2. Mavzular Qamrovi\n\nTest kasrlar mavzusining quyidagi asosiy yo'nalishlarini qamrab olgan:\n\n1.  **Oddiy kasrlarni qo'shish:**\n    *   Har xil maxrajli kasrlarni qo'shish (umumiy maxrajni topish talab etiladi).\n    *   Maxrajlardan biri ikkinchisining karralisi bo'lgan holatlar.\n2.  **Oddiy kasrlarni ayirish:**\n    *   Har xil maxrajli kasrlarni ayirish (umumiy maxrajni topish talab etiladi).\n    *   Maxrajlardan biri ikkinchisining karralisi bo'lgan holatlar.\n    *   Butun sondan kasrlarni ayirish.\n3.  **Aralash kasrlarni qo'shish:**\n    *   Aralash kasrlarni to'g'ri qo'shish, natijani soddalashtirish.\n4.  **Aralash kasrlarni ayirish:**\n    *   Aralash kasrlarni to'g'ri ayirish.\n    *   Birinchi kasrning kasr qismidan ikkinchi kasrning kasr qismini ayirib bo'lmaydigan holatlarda butun sondan qarz olish.\n5.  **Bir nechta kasrlar ustida amallar:**\n    *   Uchta kasr yoki butun son va ikkita kasr ustida ketma-ket amallar.\n6.  **Matnli masalalar:**\n    *   Kasrlarni qo'shish va ayirishga oid amaliyotga yo'naltirilgan masalalar. Bu o'quvchilarning nazariy bilimlarni amaliyotda qo'llash qobiliyatini tekshiradi.\n\n**Xulosa:** Mavzular qamrovi kasrlar ustida qo'shish va ayirish amallarini to'liq qamrab olgan. Bu o'quvchining ushbu bo'lim bo'yicha bilim va ko'nikmalarini har tomonlama baholash imkonini beradi.\n\n---\n\n## 3. Savollarning Murakkablik Darajasi\n\nTest savollari murakkablik darajasi bo'yicha quyidagicha taqsimlangan:\n\n*   **Oson darajadagi savollar (1, 2, 3, 4-savollar):** Bu savollar oddiy kasrlarni qo'shish va ayirishning asosiy qoidalarini bilishni talab qiladi. Umumiy maxrajni topish nisbatan oson bo'lgan holatlar.\n*   **O'rta darajadagi savollar (5, 6, 7, 8, 9, 11, 13, 14-savollar):** Bu savollar biroz murakkabroq hisoblashlarni (maxrajlar kattaroq yoki o'zaro tub bo'lgan holatlar), aralash kasrlar bilan ishlashni va oddiy matnli masalalarni yechishni talab qiladi. Bir nechta amalli hisoblashlar ham shu guruhga kiradi.\n*   **Qiyin darajadagi savollar (10, 12, 15-savollar):** Bu savollar aralash kasrlarni ayirishda butun sondan qarz olish kabi murakkabroq holatlarni, shuningdek, bir nechta bosqichli va murakkabroq matnli masalalarni o'z ichiga oladi. Ayniqsa, 15-savol uchburchak perimetrini topish orqali bir nechta amallarni ketma-ket bajarishni talab qiladi.\n\n**Xulosa:** Test savollarining murakkablik darajasi o'quvchilarning turli darajadagi bilim va ko'nikmalarini baholash imkonini beruvchi progressiv tuzilishga ega. Bu testning differensial xususiyatini oshiradi.\n\n---\n\n## 4. Variantlarning Sifati\n\nVariantlar (distractorlar) sifati testning muhim ko'rsatkichlaridan biridir. Ushbu testda variantlar quyidagi jihatlar bo'yicha tahlil qilindi:\n\n*   **To'g'ri javoblar:** Barcha savollarning to'g'ri javob kalitlari tekshirildi va ular to'g'ri ekanligi tasdiqlandi.\n*   **Chalg'ituvchi variantlar (distractorlar):** Ko'pgina variantlar o'quvchilarning kasrlar bilan ishlashda yo'l qo'yadigan tipik xatolariga asoslangan. Masalan:\n    *   Suratlarni va maxrajlarni shunchaki qo'shish/ayirish (1-savol A, 3-savol A, 5-savol A, 13-savol A).\n    *   Noto'g'ri umumiy maxraj topish.\n    *   Hisoblashda e'tiborsizlik yoki arifmetik xatolar.\n    *   Aralash kasrlarni noto'g'ri o'zgartirish yoki butun sondan qarz olishda xatoliklar.\n    *   Natijani soddalashtirmaslik (garchi bu testda soddalashtirilgan javoblar to'g'ri deb belgilangan bo'lsa ham, ba'zi variantlarda soddalashtirilmagan shakllar ham uchraydi, masalan, 4-savol D varianti 4/6, to'g'ri javob 1/2).\n\n**Xulosa:** Variantlar yaxshi tanlangan bo'lib, o'quvchilarning mavzuni qanchalik chuqur tushunganini aniqlashga yordam beradi. Ular shunchaki tasodifiy javoblar emas, balki o'quvchilarning noto'g'ri tushunchalari yoki xatolarini aniqlashga qaratilgan.\n\n---\n\n## 5. Testning Umumiy Sifati va Pedagogik Xulosa\n\n*   **Aniq va tushunarli savollar:** Barcha savollar aniq va tushunarli tarzda ifodalangan. Matnli masalalar ham sodda va o'quvchilarning yoshiga mos.\n*   **Tuzilishi:** Testning tuzilishi mantiqiy. Dastlabki savollar hisoblashga qaratilgan bo'lsa, keyinchalik aralash kasrlar va nihoyat matnli masalalar berilgan. Bu o'quvchining bosqichma-bosqich bilimini tekshirishga imkon beradi.\n*   **Pedagogik ahamiyati:** Ushbu test o'quvchilarning kasrlar ustida qo'shish va ayirish amallarini bajarish bo'yicha nazariy bilimlarini, amaliy ko'nikmalarini va masalalarni yechish qobiliyatini baholash uchun juda samarali vosita hisoblanadi. U o'quvchilarning qaysi turdagi kasrlar bilan ishlashda qiyinchiliklarga duch kelishini aniqlashga yordam beradi.\n*   **Rasmning mavjudligi:** 1-savolda "Test Rasm" yozuvi tushirilgan rasm mavjud, ammo u savolning mazmuniga aloqador emas. Bu ortiqcha element bo'lib, o'quvchida chalkashlik tug'dirishi mumkin.\n\n---\n\n## 6. Kamchiliklar va Takliflar\n\n**Kamchiliklar:**\n\n1.  **1-savoldagi rasm:** Savolga aloqador bo'lmagan rasmning mavjudligi testning umumiy sifatiga salbiy ta'sir ko'rsatadi. Bu o'quvchining diqqatini chalg'itishi yoki savolga rasm orqali yechim izlashga undashi mumkin.\n\n**Takliflar:**\n\n1.  **Rasmlardan foydalanish:** Agar testda rasmlardan foydalaniladigan bo'lsa, ular savolning mazmunini to'ldirishi, tushunishni osonlashtirishi yoki vizual yordam berishi kerak. Aks holda, ularni olib tashlash tavsiya etiladi.\n2.  **Mavzuni kengaytirish (ixtiyoriy):** Agar test kasrlar mavzusini to'liq qamrab olishi kerak bo'lsa, kasrlarni ko'paytirish va bo'lish amallariga oid savollarni ham kiritish mumkin. Biroq, agar test faqat qo'shish va ayirishga qaratilgan bo'lsa, bu kamchilik emas.\n3.  **Vaqt chegarasi:** Testni o'tkazishda o'quvchilarga savollar soniga mos keladigan vaqt chegarasini belgilash tavsiya etiladi.\n4.  **Natijalarni tahlil qilish:** Test natijalarini tahlil qilish orqali o'quvchilarning umumiy qiyinchiliklarini aniqlash va kelajakda o'qitish jarayonini takomillashtirish mumkin.\n\n---\n\n## Xulosa\n\nUshbu test kasrlar ustida qo'shish va ayirish amallarini baholash uchun yaxshi tuzilgan va samarali vosita hisoblanadi. Savollarning murakkablik darajasi va variantlarning sifati yuqori. Kichik kamchilik (1-savoldagi rasm) bartaraf etilsa, testning pedagogik qiymati yanada oshadi. Umuman olganda, test o'quvchilarning ushbu muhim matematik mavzudagi bilim va ko'nikmalarini aniq baholashga xizmat qiladi.	2026-06-06 11:35:18.974887+05	[{"id": 361, "question": "Hisoblang:  1/2 + 1/3 <br><img src=\\"/static/uploads/quiz_images/c4ac1c8c-28bf-4f51-b1c1-60f068772e3e.jpeg\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "2/5", "B": "5/6", "C": "2/3", "D": "1/6"}, "correct": "B", "image_path": null}, {"id": 362, "question": "Hisoblang:  3/4 - 1/2", "options": {"A": "1/4", "B": "2/2", "C": "1/2", "D": "1/8"}, "correct": "A", "image_path": null}, {"id": 363, "question": "Amalni bajaring:  2/5 + 3/10", "options": {"A": "5/15", "B": "7/10", "C": "1/2", "D": "4/5"}, "correct": "B", "image_path": null}, {"id": 364, "question": "Hisoblang:  5/6 - 1/3", "options": {"A": "4/3", "B": "1/2", "C": "2/3", "D": "4/6"}, "correct": "B", "image_path": null}, {"id": 365, "question": "Yig‘indini toping:  2/3 + 1/4", "options": {"A": "3/7", "B": "11/12", "C": "7/12", "D": "5/12"}, "correct": "B", "image_path": null}, {"id": 366, "question": "Ayirmani hisoblang:  7/8 - 2/5", "options": {"A": "5/3", "B": "9/40", "C": "19/40", "D": "5/40"}, "correct": "C", "image_path": null}, {"id": 367, "question": "Hisoblang:  1 - 2/3 - 1/6", "options": {"A": "1/6", "B": "1/3", "C": "1/2", "D": "5/6"}, "correct": "A", "image_path": null}, {"id": 368, "question": "Hisoblang:  2 1/2 + 1 1/4", "options": {"A": "3 2/6", "B": "3 3/4", "C": "3 1/2", "D": "4 1/4"}, "correct": "B", "image_path": null}, {"id": 369, "question": "Ayirmani toping:  3 2/3 - 1 1/2", "options": {"A": "2 1/6", "B": "2 1/1", "C": "1 5/6", "D": "2 1/3"}, "correct": "A", "image_path": null}, {"id": 370, "question": "Hisoblang:  4 1/5 - 2 1/2", "options": {"A": "2 3/10", "B": "1 7/10", "C": "2 1/3", "D": "1 3/10"}, "correct": "B", "image_path": null}, {"id": 371, "question": "Madina do‘kondan 3/4 kg olma va 1/2 kg banan sotib oldi. U jami necha kilogramm meva sotib olgan?", "options": {"A": "1 1/4 kg", "B": "4/6 kg", "C": "1 1/2 kg", "D": "3/8 kg"}, "correct": "A", "image_path": null}, {"id": 372, "question": "Idishda 2 1/2 litr sut bor edi. Undan pirog pishirish uchun 3/4 litr sut ishlatildi. Idishda qancha sut qoldi?", "options": {"A": "1 1/2 litr", "B": "1 3/4 litr", "C": "2 1/4 litr", "D": "1 1/4 litr"}, "correct": "B", "image_path": null}, {"id": 373, "question": "Sayyoh birinchi soatda yo‘lning 1/3 qismini, ikkinchi soatda esa 2/5 qismini bosib o‘tdi. U ikki soatda yo‘lning qancha qismini bosib o‘tgan?", "options": {"A": "3/8 qismini", "B": "11/15 qismini", "C": "2/15 qismini", "D": "4/5 qismini"}, "correct": "B", "image_path": null}, {"id": 374, "question": "Hovuzdagi suvning 5/8 qismi to‘ldirilgan. Quyosh issig‘ida suvning 1/4 qismi bug‘lanib ketdi. Hovuzning qancha qismida suv qoldi?", "options": {"A": "4/4 qismi", "B": "1/2 qismi", "C": "3/8 qismi", "D": "1/8 qismi"}, "correct": "C", "image_path": null}, {"id": 375, "question": "Uchburchakning birinchi tomoni 1/2 m, ikkinchi tomoni birinchisidan 1/5 m uzun, uchinchi tomoni esa 3/10 m. Uchburchakning perimetrini toping.", "options": {"A": "1 1/2 m", "B": "1 m", "C": "1 2/5 m", "D": "9/10 m"}, "correct": "A", "image_path": null}]
15	\N	\N	Xatolik: AI tahlil qilish vaqti tugadi (Timeout).	2026-06-06 22:28:48.931965+05	[{"id": 376, "question": "1. Eng kichik besh xonali natural son bilan eng katta to'rt xonali natural sonning ayirmasini toping.", "options": {"A": "1", "B": "10", "C": "9", "D": "0"}, "correct": "A", "image_path": null}, {"id": 377, "question": "2. 0, 3, 4, 7 raqamlaridan foydalanib (raqamlar takrorlanishi mumkin) yozish mumkin bo'lgan eng kichik uch xonali natural sonni toping.", "options": {"A": "300", "B": "303", "C": "100", "D": "347"}, "correct": "A", "image_path": null}, {"id": 378, "question": "3. Quyidagi rasmda natural sonlar o‘qining bir qismi tasvirlangan. Nuqtalar o‘rniga mos keluvchi natural sonlar yig‘indisini toping.<br><img src=\\"/static/uploads/quiz_images/ef56f547-41db-4136-b388-58676c0de095.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "24", "B": "22", "C": "26", "D": "25"}, "correct": "A", "image_path": null}, {"id": 379, "question": "4. Raqamlari takrorlanmaydigan eng katta uch xonali natural sonni ko'rsating.", "options": {"A": "987", "B": "999", "C": "989", "D": "897"}, "correct": "A", "image_path": null}, {"id": 380, "question": "5. Natural sonlar qatorida 45 va 75 sonlari orasida nechta natural son mavjud? (45 va 75 sonlarining o'zi bu hisobga kirmaydi)", "options": {"A": "29 ta", "B": "30 ta", "C": "31 ta", "D": "28 ta"}, "correct": "A", "image_path": null}, {"id": 381, "question": "6. 3 raqami bilan tugaydigan barcha ikki xonali natural sonlar nechta?", "options": {"A": "9 ta", "B": "10 ta", "C": "8 ta", "D": "11 ta"}, "correct": "A", "image_path": null}, {"id": 382, "question": "7. Dastlabki 15 ta natural son ichida nechta juft son mavjud?", "options": {"A": "7 ta", "B": "8 ta", "C": "6 ta", "D": "9 ta"}, "correct": "A", "image_path": null}, {"id": 383, "question": "8. Quyidagi abak (cho‘t) rasmida qaysi natural son tasvirlanganini aniqlang.<br><img src=\\"/static/uploads/quiz_images/568beb7a-0a08-4cfa-a7bb-8246991e2e5c.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "3042", "B": "3420", "C": "342", "D": "30420"}, "correct": "A", "image_path": null}, {"id": 384, "question": "9. 8654 sonida jami nechta yuzlik xona birligi bor?", "options": {"A": "6 ta", "B": "60 ta", "C": "86 ta", "D": "5 ta"}, "correct": "C", "image_path": null}, {"id": 386, "question": "11. Berilgan sonni xona qo'shiluvchilari yig'indisi ko'rinishida yozing: 9050 = ?", "options": {"A": "9000 + 50", "B": "900 + 50", "C": "9000 + 500", "D": "9000 + 5"}, "correct": "A", "image_path": null}, {"id": 387, "question": "12. 6328 sonining yuzliklar xonasida turgan raqamning xona qiymati qanchaga teng?", "options": {"A": "300", "B": "3", "C": "30", "D": "600"}, "correct": "A", "image_path": null}, {"id": 388, "question": "13. Ikki xonali sonning o'nliklar xonasidagi raqam birliklar xonasidagi raqamdan 4 marta kichik. Bu qaysi son bo'lishi mumkin?", "options": {"A": "28", "B": "41", "C": "82", "D": "12"}, "correct": "A", "image_path": null}, {"id": 389, "question": "14. Bir sonning minglar xonasidagi raqam 5 ga, o'nlar xonasidagi raqam 2 ga teng, qolgan xonalari esa 0. Shu sonni toping.", "options": {"A": "5020", "B": "5200", "C": "5002", "D": "520"}, "correct": "A", "image_path": null}, {"id": 390, "question": "15. Rasmda uchta xona birligi kubiklar shaklida ko‘rsatilgan. Kubiklar yordamida hosil qilingan umumiy sonni toping.<br><img src=\\"/static/uploads/quiz_images/78236c29-6749-4970-91c9-6b4fdf0f9fe1.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "235", "B": "253", "C": "325", "D": "532"}, "correct": "A", "image_path": null}, {"id": 391, "question": "16. Qo'shish amalida birinchi qo'shiluvchi 480 ga teng. Agar yig'indi 920 bo'lsa, ikkinchi qo'shiluvchini aniqlang.", "options": {"A": "440", "B": "460", "C": "540", "D": "1400"}, "correct": "A", "image_path": null}, {"id": 392, "question": "17. Berilgan sxemadagi matematik zanjirni hisoblang va so‘roq belgisi (?) o‘rnidagi sonni toping.<br><img src=\\"/static/uploads/quiz_images/71b74bd7-f673-4be2-9f45-b348fccb14a1.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "750", "B": "850", "C": "1650", "D": "650"}, "correct": "A", "image_path": null}, {"id": 393, "question": "18. Agar kamayuvchini 50 ga oshirib, ayriluvchini o'zgarishsiz qoldirsak, ayirma qanday o'zgaradi?", "options": {"A": "50 ga ortadi", "B": "50 ga kamayadi", "C": "O'zgarmaydi", "D": "100 ga ortadi"}, "correct": "A", "image_path": null}, {"id": 394, "question": "19. Rasmda tarozining ikki pallasi muvozanatda turibdi. Chap palladagi noma’lum yukning x og‘irligini toping.<br><img src=\\"/static/uploads/quiz_images/d61c319d-983b-41fd-89cf-b194770a1352.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "25 kg", "B": "75 kg", "C": "15 kg", "D": "30 kg"}, "correct": "A", "image_path": null}, {"id": 395, "question": "20. Uchta sonning yig'indisi 1500 ga teng. Birinchi son 420, ikkinchi son 580 bo'lsa, uchinchi sonni toping.", "options": {"A": "500", "B": "400", "C": "600", "D": "1000"}, "correct": "A", "image_path": null}, {"id": 396, "question": "21. Ikki sonning ayirmasi 180 ga teng. Agar ayriluvchi 320 bo'lsa, kamayuvchini toping.", "options": {"A": "500", "B": "140", "C": "400", "D": "480"}, "correct": "A", "image_path": null}, {"id": 397, "question": "22. Yig'indisi 840 ga teng bo'lgan ikki sonning biri ikkinchisidan 140 ga katta. Kichik sonni toping.", "options": {"A": "350", "B": "490", "C": "420", "D": "300"}, "correct": "A", "image_path": null}, {"id": 398, "question": "23. Omborda 850 kg un bor edi. Grafikda unning sarflanishi ko‘rsatilgan. Omborda necha kilogramm un qoldi?<br><img src=\\"/static/uploads/quiz_images/d9557a22-3369-4f6a-8c92-f348029a0775.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "300 kg", "B": "310 kg", "C": "550 kg", "D": "290 kg"}, "correct": "A", "image_path": null}, {"id": 399, "question": "24. Birinchi moshina ombordan 320 ta gisht, ikkinchi moshina esa birinchisiga qaraganda 60 ta ko'p gisht tashidi. Ikki moshina birgalikda jami nechta gisht tashigan?", "options": {"A": "700 ta", "B": "380 ta", "C": "640 ta", "D": "760 ta"}, "correct": "A", "image_path": null}, {"id": 400, "question": "25. Quyidagi rasmda do‘kondagi mahsulotlar narxi berilgan. 2 ta daftar va 3 ta ruchka sotib olish uchun jami qancha pul to'lash kerak?<br><img src=\\"/static/uploads/quiz_images/9078a3c2-4a1c-4892-b523-30403aa75fef.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "4800 so'm", "B": "4400 so'm", "C": "5200 so'm", "D": "4000 so'm"}, "correct": "A", "image_path": null}, {"id": 401, "question": "26. Kitob javonining birinchi g'aladonida 48 ta kitob bor. Ikkinchi g'aladondagi kitoblar soni birinchisidan 12 ta kam, uchinchi g'aladonda esa ikkinchisidan 15 ta ko'p kitob bor. Uchinchi g'aladonda nechta kitob bor?", "options": {"A": "51 ta", "B": "36 ta", "C": "45 ta", "D": "63 ta"}, "correct": "A", "image_path": null}, {"id": 402, "question": "27. Sayyoh chizmadagi A punktdan B punktga, keyin C punktga qarab yurdi. Sayyoh jami qancha masofani bosib o'tgan?<br><img src=\\"/static/uploads/quiz_images/55c4b113-b041-4003-8139-934c2b901244.png\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "50 km", "B": "22 km", "C": "56 km", "D": "48 km"}, "correct": "A", "image_path": null}, {"id": 403, "question": "28. Tikuvchilik sexida 450 metr mato bor edi. Maktab formalari uchun 180 metr, ko'ylaklar uchun esa 140 metr mato sarflandi. Sexda necha metr mato qoldi?", "options": {"A": "130 m", "B": "150 m", "C": "320 m", "D": "120 m"}, "correct": "A", "image_path": null}, {"id": 385, "question": "10. Rasmda berilgan xonalar jadvalidagi yashirin sonning o‘nliklar xonasidagi raqamni 3 taga oshirsak, son qiymati qanchaga ortadi? <br><img src=", "options": {"A": "30 ga", "B": "3 ga", "C": "300 ga", "D": "3000 ga"}, "correct": "A", "image_path": null}, {"id": 404, "question": "29. Sinfdagi o‘quvchilar tarkibi diagrammada ko‘rsatilgan. Agar jami o'quvchilar soni 32 ta bo'lib, o'g'il bolalar qizlardan 4 taga ko'p bo'lsa, sinfda nechta qiz bola bor?", "options": {"A": "14 ta", "B": "18 ta", "C": "16 ta", "D": "15 ta"}, "correct": "A", "image_path": null}, {"id": 405, "question": "30. Do'konga 600 ta daftar olib kelindi. Birinchi hafta 230 ta, ikkinchi hafta esa birinchi haftadagidan 40 ta kam daftar sotildi. Do'konda sotilmay qolgan nechta daftar qoldi?", "options": {"A": "180 ta", "B": "190 ta", "C": "420 ta", "D": "210 ta"}, "correct": "A", "image_path": null}]
21	\N	\N	Ushbu test savollari to‘plamini metodik nuqtai nazardan tahlil qilib, quyidagi xulosalarni taqdim etaman:\n\n### **1. Testning umumiy tavsifi va yo‘nalishi**\nUshbu testlar to‘plami asosan **"Amaliy matematika va mantiqiy hisoblashlar"** yo‘nalishiga qaratilgan. Savollar IT sohasi, muhandislik va texnik jarayonlar (server xonalari, ma’lumotlar uzatish tezligi, fizik kattaliklar, vaqt va hajm o‘lchovlari) kontekstida tuzilgani juda ijobiy holat. Bu o‘quvchining nazariy bilimlarni real hayotiy va kasbiy vaziyatlarga tatbiq eta olish qobiliyatini tekshiradi.\n\n### **2. Mavzular qamrovi**\nTest quyidagi asosiy mavzularni qamrab olgan:\n*   **O‘lchov birliklarini konvertatsiya qilish:** (MB/GB, sm/m/dm, minut/soat/sutka, tonna/kg).\n*   **Geometrik hisoblashlar:** (Yuzani, hajmni, perimetrni topish).\n*   **Fizik kattaliklar:** (Zichlik, massa, tezlik, vaqt).\n*   **Proporsiya va foizlar:** (Ish unumdorligi, sarf-xarajatlar).\n*   **Mantiqiy masalalar:** (Poyezdning tunneldan o‘tishi, skript so‘rovlari).\n\n### **3. Murakkablik darajasi**\n*   **Daraja:** O‘rta va yuqori.\n*   **Tahlil:** Savollar shunchaki formulani yodlashni emas, balki bir necha bosqichli mantiqiy fikrlashni talab qiladi (masalan, 13-savolda KB dan MB ga o‘tish va vaqtni minutga aylantirish). Bu o‘quvchining diqqat-e’tiborini va matematik savodxonligini yaxshi tekshiradi.\n\n### **4. Test sifati va variantlar tahlili**\n*   **Ijobiy tomonlari:**\n    *   **Kontekst:** Savollar IT va texnika sohasiga moslashtirilgani o‘quvchida qiziqish uyg‘otadi.\n    *   **Aniqlik:** Barcha savollarda o‘lchov birliklari (1 GB = 1000 MB kabi) aniq ko‘rsatilgan, bu esa noaniqliklarning oldini oladi.\n    *   **Chalg‘ituvchi variantlar:** Noto‘g‘ri javob variantlari tasodifiy emas, balki o‘quvchi hisoblashda yo‘l qo‘yishi mumkin bo‘lgan tipik xatolar (masalan, birliklarni o‘zgartirishni unutish) asosida tuzilgan. Bu testning sifatini oshiradi.\n*   **Kamchiliklar va tavsiyalar:**\n    *   **Javob kaliti:** Barcha 20 ta savolning to‘g‘ri javobi "A" varianti qilib belgilangan. Bu **jiddiy metodik xato**. Testni yechayotgan o‘quvchi buni sezib qolsa, mantiqiy fikrlashni to‘xtatib, barchasini "A" deb belgilab ketishi mumkin. **Tavsiya:** Javob variantlarini aralashtirib chiqish (A, B, C, D ketma-ketligini o‘zgartirish) shart.\n\n### **5. Pedagogik xulosa**\nUshbu testlar to‘plami o‘zining mazmuni va murakkabligi bo‘yicha **juda yuqori sifatli**. U o‘quvchining nafaqat matematik qobiliyatini, balki texnik tafakkurini ham rivojlantiradi.\n\n**Yakuniy baho:**\n*   **Mazmunan:** 10/10\n*   **Texnik tuzilishi (variantlar joylashuvi):** 2/10 (Javoblar ketma-ketligi o‘zgartirilishi kerak).\n*   **Tavsiya:** Savollarning o‘zini o‘zgartirmasdan, faqat variantlar tartibini (to‘g‘ri javobni har xil harflarga taqsimlab) qayta tahrirlash kifoya.\n\nUshbu testlar o‘quvchilarni real loyihaviy ishlarga tayyorlash uchun ajoyib vosita bo‘lib xizmat qiladi.	2026-06-07 22:36:15.947584+05	[{"id": 406, "question": "Ma'lumot sekundiga 2.5 megabayt (MB) tezlikda yuklanadi. Hajmi 0.012 gigabayt (GB) bo‘lgan fayl to‘liq yuklanishi uchun necha sekund vaqt ketadi? (1 GB = 1000 MB)", "options": {"A": "4.8 sekund", "B": "3 sekund", "C": "48 sekund", "D": "0.48 sekund"}, "correct": "A", "image_path": null}, {"id": 407, "question": "To‘g‘ri burchakli parallelepiped shaklidagi serverlar xonasining o‘lchamlari: bo‘yi 500 sm, eni 4 m va balandligi 30 dm. Ushbu xonaning umumiy hajmini metr kub (m³) larda hisoblang.", "options": {"A": "60 m³", "B": "600 m³", "C": "6 m³", "D": "60,000 m³"}, "correct": "A", "image_path": null}, {"id": 408, "question": "Xaritada server markazi joylashgan maydon to‘g‘ri to‘rtburchak shaklida bo‘lib, uning yuzi 24 sm² ga teng. Xaritaning masshtabi 1:1000 bo‘lsa, ushbu markazning haqiqiy maydoni necha metr kvadrat (m²) bo‘ladi?", "options": {"A": "2400 m²", "B": "240 m²", "C": "24 m²", "D": "24,000 m²"}, "correct": "C", "image_path": null}, {"id": 409, "question": "Omborga jami 3.2 tonna kompyuter jihozlari keltirildi. Ularning 45% ini monitorlar, qolgan qismini tizimli bloklar tashkil etadi. Keltirilgan tizimli bloklarning umumiy massasi necha kilogramm (kg)?", "options": {"A": "1760 kg", "B": "1440 kg", "C": "176 kg", "D": "1800 kg"}, "correct": "A", "image_path": null}, {"id": 410, "question": "Uchta dasturchi birgalikda ishladi. Birinchisi loyiha ustida 2 sutka, ikkinchisi 15 soat, uchinchisi esa 2100 minut vaqt sarfladi. Ular jami bo‘lib loyiha ustida necha soat ishlagan?", "options": {"A": "98 soat", "B": "102 soat", "C": "88 soat", "D": "95 soat"}, "correct": "A", "image_path": null}, {"id": 411, "question": "Skript har 15 millisekundda bitta so‘rov yuboradi. Ushbu skript 3 minut davomida jami nechta so‘rov yuborishga ulguradi?", "options": {"A": "12,000 ta", "B": "1,200 ta", "C": "18,000 ta", "D": "20,000 ta"}, "correct": "A", "image_path": null}, {"id": 412, "question": "Zichligi 0.8 g/sm³ bo‘lgan maxsus suyuqlik 5 litrli sovutish tizimi idishini to‘liq to‘ldiradi. Idishdagi suyuqlikning umumiy massasi necha kilogramm (kg) bo‘ladi?", "options": {"A": "4 kg", "B": "40 kg", "C": "0.4 kg", "D": "4.5 kg"}, "correct": "A", "image_path": null}, {"id": 413, "question": "Kabelning 1 metri 120 gramm tosh bosadi. Umumiy massasi 0.18 tonna bo‘lgan kabel g‘altagida necha metr kabel mavjud?", "options": {"A": "1500 m", "B": "150 m", "C": "15,000 m", "D": "1200 m"}, "correct": "A", "image_path": null}, {"id": 414, "question": "Avtomatlashtirilgan tizim xonadagi haroratni har 45 minutda o‘lchaydi. Tizim 6 sutka davomida jami necha marta haroratni o‘lchashni amalga oshiradi?", "options": {"A": "192 marta", "B": "96 marta", "C": "144 marta", "D": "200 marta"}, "correct": "A", "image_path": null}, {"id": 415, "question": "Kvadrat shaklidagi ma'lumotlar markazi er maydonining perimetri 0.36 km ga teng. Ushbu markazning umumiy er maydoni necha metr kvadrat (m²) bo‘ladi?", "options": {"A": "8100 m²", "B": "32,400 m²", "C": "900 m²", "D": "1296 m²"}, "correct": "A", "image_path": null}, {"id": 416, "question": "Ekranning o‘lchami 40 sm va 30 sm ga teng. Agar uning yuzasining har bir kvadrat santimetrida (sm²) 64 ta piksel joylashgan bo‘lsa, ekrandagi jami piksellar soni nechta?", "options": {"A": "76,800 ta", "B": "1200 ta", "C": "7680 ta", "D": "19,200 ta"}, "correct": "A", "image_path": null}, {"id": 417, "question": "Hajmi 1.2 litr bo‘lgan konteyner mikrochiplar bilan to‘ldirilgan. Bitta chipning hajmi 150 mm³ bo‘lsa, ushbu konteynerga jami nechta chip joylashgan? (1 litr = 1 dm³)", "options": {"A": "8,000,000 ta", "B": "8,000 ta", "C": "80,000 ta", "D": "800,000 ta"}, "correct": "C", "image_path": null}, {"id": 418, "question": "Eski qattiq disk ma'lumotni sekundiga 400 kilobayt (KB) tezlikda nusxalaydi. 0.2 gigabayt (GB) hajmdagi faylni nusxalash uchun diskka necha minut vaqt kerak bo‘ladi? (1 GB = 1000 MB, 1 MB = 1000 KB)", "options": {"A": "8.33 minut", "B": "5 minut", "C": "500 minut", "D": "83.3 minut"}, "correct": "A", "image_path": null}, {"id": 419, "question": "Lazerli kesgich metall listni minutiga 25 sm tezlik bilan kesadi. Uzunligi 0.015 km bo‘lgan metall chiziqni to‘liq kesib chiqish uchun lazer necha soat ishlashi kerak?", "options": {"A": "1 soat", "B": "0.6 soat", "C": "10 soat", "D": "2.5 soat"}, "correct": "A", "image_path": null}, {"id": 420, "question": "Yengil qotishmadan yasalgan detalning massasi 450 gramm bo‘lib, hajmi 150 sm³ ga teng. Ushbu qotishmaning zichligini kg/m³ (metr kub taqsim kilogramm) birligida ko‘rsating.", "options": {"A": "3000 kg/m³", "B": "300 kg/m³", "C": "30 kg/m³", "D": "30,000 kg/m³"}, "correct": "A", "image_path": null}, {"id": 421, "question": "Hovuzdagi suv nasos yordamida minutiga 250 litr tezlikda bo‘shatilyapti. Hovuzda jami 45 m³ suv bo‘lsa, uni to‘liq bo‘shatish uchun necha soat vaqt talab etiladi?", "options": {"A": "3 soat", "B": "2.5 soat", "C": "180 soat", "D": "4.5 soat"}, "correct": "A", "image_path": null}, {"id": 422, "question": "Dastur ishga tushgandan so‘ng server xotirasidan dastlabki 4 minutda har sekundda 15 kilobayt (KB) joy band qila boshladi. Dastur shu vaqt ichida jami necha megabayt (MB) xotirani band qilgan? (1 MB = 1000 KB)", "options": {"A": "3.6 MB", "B": "36 MB", "C": "0.36 MB", "D": "360 MB"}, "correct": "A", "image_path": null}, {"id": 423, "question": "To‘g‘ri to‘rtburchak shaklidagi quyosh panellarining bo‘yi 250 sm, eni esa 12 dm. Jami 20 ta shunday panel keltirilgan bo‘lsa, ularning umumiy yuzasi necha metr kvadrat (m²) bo‘ladi?", "options": {"A": "60 m²", "B": "6 m²", "C": "600 m²", "D": "30 m²"}, "correct": "A", "image_path": null}, {"id": 424, "question": "Laboratoriya qurilmasi har sutkada 15 gramm maxsus gaz sarflaydi. Ballon ichida 1.35 kg gaz bor bo‘lsa, ushbu zaxira qurilmaga necha hafta ishlashga yetadi?", "options": {"A": "12 hafta", "B": "90 hafta", "C": "15 hafta", "D": "13 hafta"}, "correct": "A", "image_path": null}, {"id": 425, "question": "Uzunligi 480 metr bo‘lgan poyezd tunneldan 72 km/soat tezlikda o‘tmoqda. Agar poyezd tunnelga kirishni boshlaganidan to to‘liq chiqib ketgunicha 1 minut vaqt ketgan bo‘lsa, tunnelning uzunligi necha metr?", "options": {"A": "720 m", "B": "1200 m", "C": "640 m", "D": "1680 m"}, "correct": "A", "image_path": null}]
22	\N	\N	Assalomu alaykum. Tajribali metodist sifatida taqdim etilgan test savollarini tahlil qildim. Quyida ushbu testlar bo'yicha pedagogik xulosa va har bir savolning yechimi keltirilgan.\n\n---\n\n### 📊 Pedagogik Tahlil va Xulosa\n\n**1. Mavzular qamrovi:**\nTestlar asosan algebra kursining boshlang'ich va o'rta bosqich mavzularini qamrab olgan:\n*   Bir o'zgaruvchili chiziqli tenglamalar.\n*   Qavslarni ochish va o'xshash hadlarni ixchamlash.\n*   Kvadrat tenglamalar (to'liq va chala).\n*   Kasrli tenglamalar (sodda ko'rinishda).\n\n**2. Murakkablik darajasi:**\nTestlar asosan "o'rta" va "oson" darajadagi savollardan iborat. Bu o'quvchining bazaviy bilimlarini tekshirish uchun juda mos keladi. Savollar ketma-ketligi mantiqiy ravishda oddiydan murakkabroqqa qarab boradi.\n\n**3. Test sifati va tavsiyalar:**\n*   **Ijobiy tomoni:** Savollar aniq va tushunarli. Variantlar chalg'ituvchi (distraktorlar) sifatida yaxshi tanlangan (masalan, kvadrat tenglamalarda ishoralarni almashtirib qo'yish).\n*   **Kamchilik:** 18-savolning sharti noto'g'ri shakllantirilgan ("B javob to'g'ri" deb yozilgan, bu test savoli emas, balki tasdiq).\n*   **Tavsiya:** Testlar bazasini boyitish uchun matnli masalalarni (tenglamaga keltiriladigan) qo'shish maqsadga muvofiq bo'lardi.\n\n---\n\n### ✅ Savollar tahlili va to'g'ri javoblar\n\n| Savol № | To'g'ri javob | Izoh / Yechim |\n| :--- | :--- | :--- |\n| 1 | **B** | 8x = 16 => x = 2 |\n| 2 | **B** | 2a + 8 - 3a = 5 => -a = -3 => a = 3 |\n| 3 | **A** | (x+2)(x+3)=0 => x1=-2, x2=-3 |\n| 4 | **C** | 4y - 2y + 6 = 20 => 2y = 14 => y = 7 |\n| 5 | **B** | 3x^2 - 6x = 3x^2 - 12 => -6x = -12 => x = 2 |\n| 6 | **C** | a^2 = 9 => a = ±3 |\n| 7 | **C** | 4z = 24 => z = 6 |\n| 8 | **B** | 6k + 2 = 20 => 6k = 18 => k = 3 |\n| 9 | **B** | (3x+2x)/6 = 10 => 5x = 60 => x = 12 |\n| 10 | **C** | 3m = 21 => m = 7 |\n| 11 | **B** | p - 5 = 2 => p = 7 |\n| 12 | **C** | n^2 = 16 => n = ±4 |\n| 13 | **C** | 6y = 36 => y = 6 |\n| 14 | **A** | (x-1)^2 = 0 => x = 1 |\n| 15 | **B** | 6a = 12 => a = 2 |\n| 16 | **B** | 10 - 2x - 2 = 4 => 8 - 2x = 4 => 2x = 4 => x = 2 |\n| 17 | **B** | 6c - 12 = 6 => 6c = 18 => c = 3 |\n| 18 | **B** | Savol sharti noaniq, lekin B javob tanlangan. |\n| 19 | **B** | 6x + 12 = 4x + 20 => 2x = 8 => x = 4 |\n| 20 | **C** | b^2 = 25 => b = ±5 |\n\n*Izoh: 18-savol bo'yicha metodik tavsiyam: uni matematik ifoda ko'rinishida (masalan, 3b - 2 = 10) qayta shakllantirish kerak.*	2026-06-11 18:05:22.671993+05	[{"id": 426, "question": "Ifodani soddalashtiring va tenglamani yeching: 3x + 5x - 2 = 14", "options": {"A": "x = 1", "B": "x = 2", "C": "x = 3", "D": "x = 4"}, "correct": "B", "image_path": null}, {"id": 427, "question": "Ifodani soddalashtiring va tenglamani yeching: 2(a + 4) - 3a = 5", "options": {"A": "a = 2", "B": "a = 3", "C": "a = -3", "D": "a = -2"}, "correct": "B", "image_path": null}, {"id": 428, "question": "Ifodani soddalashtiring va tenglamani yeching: x^2 + 5x + 6 = 0", "options": {"A": "x1 = -2, x2 = -3", "B": "x1 = 2, x2 = 3", "C": "x1 = 1, x2 = 6", "D": "x1 = -1, x2 = -6"}, "correct": "A", "image_path": null}, {"id": 430, "question": "Ifodani soddalashtiring va tenglamani yeching: 4y - (2y - 6) = 20", "options": {"A": "y = 5", "B": "y = 6", "C": "y = 7", "D": "y = 8"}, "correct": "C", "image_path": null}, {"id": 431, "question": "Ifodani soddalashtiring va tenglamani yeching: 3x(x - 2) = 3x^2 - 12", "options": {"A": "x = 1", "B": "x = 2", "C": "x = 3", "D": "x = 4"}, "correct": "B", "image_path": null}, {"id": 432, "question": "Ifodani soddalashtiring va tenglamani yeching: a^2 - 9 = 0", "options": {"A": "a = 3", "B": "a = -3", "C": "a = ±3", "D": "a = 9"}, "correct": "C", "image_path": null}, {"id": 433, "question": "Ifodani soddalashtiring va tenglamani yeching: 7z - 3z = 24", "options": {"A": "z = 4", "B": "z = 5", "C": "z = 6", "D": "z = 7"}, "correct": "C", "image_path": null}, {"id": 434, "question": "Ifodani soddalashtiring va tenglamani yeching: 2(3k + 1) = 20", "options": {"A": "k = 2", "B": "k = 3", "C": "k = 4", "D": "k = 1"}, "correct": "B", "image_path": null}, {"id": 435, "question": "Ifodani soddalashtiring va tenglamani yeching: x/2 + x/3 = 10", "options": {"A": "x = 10", "B": "x = 12", "C": "x = 15", "D": "x = 18"}, "correct": "B", "image_path": null}, {"id": 436, "question": "Ifodani soddalashtiring va tenglamani yeching: 5m - 2m + 8 = 29", "options": {"A": "m = 5", "B": "m = 6", "C": "m = 7", "D": "m = 8"}, "correct": "C", "image_path": null}, {"id": 437, "question": "Ifodani soddalashtiring va tenglamani yeching: 4(p - 5) = 8", "options": {"A": "p = 6", "B": "p = 7", "C": "p = 8", "D": "p = 9"}, "correct": "B", "image_path": null}, {"id": 438, "question": "Ifodani soddalashtiring va tenglamani yeching: n^2 - 16 = 0", "options": {"A": "n = 4", "B": "n = -4", "C": "n = ±4", "D": "n = 16"}, "correct": "C", "image_path": null}, {"id": 440, "question": "Ifodani soddalashtiring va tenglamani yeching: 9y - 3y = 36", "options": {"A": "y = 4", "B": "y = 5", "C": "y = 6", "D": "y = 7"}, "correct": "C", "image_path": null}, {"id": 441, "question": "Ifodani soddalashtiring va tenglamani yeching: x^2 - 2x + 1 = 0", "options": {"A": "x = 1", "B": "x = -1", "C": "x = 2", "D": "x = 0"}, "correct": "A", "image_path": null}, {"id": 442, "question": "Ifodani soddalashtiring va tenglamani yeching: 2a + 5a - a = 12", "options": {"A": "a = 1", "B": "a = 2", "C": "a = 3", "D": "a = 4"}, "correct": "B", "image_path": null}, {"id": 443, "question": "Ifodani soddalashtiring va tenglamani yeching: 10 - 2(x + 1) = 4", "options": {"A": "x = 1", "B": "x = 2", "C": "x = 3", "D": "x = 4"}, "correct": "B", "image_path": null}, {"id": 445, "question": "Ifodani soddalashtiring va tenglamani yeching: 3(2c - 4) = 6", "options": {"A": "c = 2", "B": "c = 3", "C": "c = 4", "D": "c = 5"}, "correct": "B", "image_path": null}, {"id": 429, "question": "Ifodani soddalashtiring va tenglamani yeching: B jabov to'g'ri", "options": {"A": "b = 3", "B": "b = 4", "C": "b = 5", "D": "b = 2"}, "correct": "B", "image_path": null}, {"id": 439, "question": "Ifodani soddalashtiring va tenglamani yeching: 6(x + 2) = 4(x + 5)", "options": {"A": "x = 3", "B": "x = 4", "C": "x = 5", "D": "x = 6"}, "correct": "B", "image_path": null}, {"id": 444, "question": "Ifodani soddalashtiring va tenglamani yeching: b^2 - 25 = 0", "options": {"A": "b = 5", "B": "b = -5", "C": "b = 5", "D": "b = 25"}, "correct": "C", "image_path": null}]
23	\N	\N	Assalomu alaykum. Tajribali metodist sifatida taqdim etilgan test savollarini pedagogik nuqtai nazardan tahlil qildim. Quyida ushbu tahlil va savollarning to‘g‘ri javoblari keltirilgan.\n\n---\n\n### 📊 Pedagogik Tahlil\n\n**1. Mavzu qamrovi:**\nTest savollari matematika fanining boshlang‘ich sinf dasturiga oid "Sonlarni yuzliklar xonasigacha yaxlitlash" mavzusini to‘liq qamrab olgan. Savollar o‘quvchining yaxlitlash qoidalarini (o‘nliklar xonasidagi raqam 5 dan kichik bo‘lsa – pastga, 5 va undan katta bo‘lsa – yuqoriga yaxlitlash) qay darajada o‘zlashtirganini tekshirishga qaratilgan.\n\n**2. Murakkablik darajasi:**\nTest savollari asosan **"o‘rta"** va **"oson"** darajada. Savollar ketma-ketligi mantiqiy tuzilgan. Ayniqsa, 5-savol (999) va 10-savol (1049) o‘quvchining diqqatini tekshirish uchun yaxshi tanlangan, chunki bu yerda xonalar o‘tishi (o‘nlikdan yuzlikka, yuzlikdan minglikka) mavjud.\n\n**3. Variantlar sifati:**\n*   **Chalg‘ituvchi variantlar (distraktorlar):** Variantlar yaxshi tanlangan. Masalan, 145 sonida 150 (o‘nliklargacha yaxlitlash) yoki 140 (xato yaxlitlash) kabi variantlar o‘quvchining xato qilish ehtimoli bo‘lgan joylarni qamrab olgan.\n*   **Texnik xatolik:** 1-savolda kichik bir noaniqlik bor. 145 sonini yuzliklargacha yaxlitlaganda, matematik qoidaga ko‘ra 100 bo‘ladi, lekin ko‘plab darsliklarda 5 raqami kelganda yuqoriga yaxlitlash qabul qilingan (150). Biroq, siz taqdim etgan kalit bo‘yicha 100 deb olingan, bu ham qabul qilinishi mumkin bo‘lgan yondashuvdir.\n\n**4. Umumiy xulosa:**\nTest o‘z maqsadiga yetgan. U o‘quvchining mavzuni tushunish darajasini aniqlash uchun yetarli darajada sifatli tuzilgan.\n\n---\n\n### ✅ Savollar va To‘g‘ri Javoblar\n\n| Savol № | Savol mazmuni | To‘g‘ri javob |\n| :--- | :--- | :--- |\n| 1 | 145 sonini yuzliklargacha yaxlitlang | **A) 100** |\n| 2 | 872 sonini yuzliklargacha yaxlitlang | **C) 900** |\n| 3 | 329 sonini yuzliklargacha yaxlitlang | **A) 300** |\n| 4 | 550 sonini yuzliklargacha yaxlitlang | **C) 600** |\n| 5 | 999 sonini yuzliklargacha yaxlitlang | **B) 1000** |\n| 6 | 214 sonini yuzliklargacha yaxlitlang | **A) 200** |\n| 7 | 683 sonini yuzliklargacha yaxlitlang | **C) 700** |\n| 8 | 445 sonini yuzliklargacha yaxlitlang | **A) 400** |\n| 9 | 751 sonini yuzliklargacha yaxlitlang | **C) 800** |\n| 10 | 1049 sonini yuzliklargacha yaxlitlang | **A) 1000** |\n\n---\n**Metodist tavsiyasi:** Kelgusida test tuzishda 5 raqami bilan tugaydigan sonlarni (145, 445, 550) yaxlitlashda o‘quvchilarga qaysi qoidadan foydalanish (yuqoriga yoki pastga) oldindan tushuntirilgan bo‘lishi kerak, chunki bu matematikada bahsli nuqta hisoblanadi.	2026-06-11 18:07:34.733136+05	[{"id": 446, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 145 ?", "options": {"A": "100", "B": "150", "C": "200", "D": "140"}, "correct": "A", "image_path": null}, {"id": 447, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 872 ?", "options": {"A": "800", "B": "870", "C": "900", "D": "880"}, "correct": "C", "image_path": null}, {"id": 448, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 329 ?", "options": {"A": "300", "B": "320", "C": "330", "D": "400"}, "correct": "A", "image_path": null}, {"id": 449, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 550 ?", "options": {"A": "500", "B": "540", "C": "600", "D": "560"}, "correct": "C", "image_path": null}, {"id": 450, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 999 ?", "options": {"A": "900", "B": "1000", "C": "990", "D": "950"}, "correct": "B", "image_path": null}, {"id": 451, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 214 ?", "options": {"A": "200", "B": "210", "C": "220", "D": "300"}, "correct": "A", "image_path": null}, {"id": 452, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 683 ?", "options": {"A": "600", "B": "680", "C": "700", "D": "690"}, "correct": "C", "image_path": null}, {"id": 453, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 445 ?", "options": {"A": "400", "B": "440", "C": "450", "D": "500"}, "correct": "A", "image_path": null}, {"id": 454, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 751 ?", "options": {"A": "700", "B": "750", "C": "800", "D": "760"}, "correct": "C", "image_path": null}, {"id": 455, "question": "Sonlarni Yuzliklar xonasigacha yaxlitlang: 1049 ?", "options": {"A": "1000", "B": "1040", "C": "1050", "D": "1100"}, "correct": "A", "image_path": null}]
26	\N	\N	Assalomu alaykum. Tajribali metodist sifatida taqdim etilgan test savollarini tahlil qildim. Quyida ushbu test bo'yicha pedagogik xulosa va tahlilni taqdim etaman.\n\n---\n\n### 1. Pedagogik tahlil va xulosa\n\n**Mavzu qamrovi:**\nTest to'liq ingliz tilidagi **"Quantifiers" (Miqdor bildiruvchi so'zlar)** mavzusiga, xususan, *some, any, much, many* va ularning ishlatilish qoidalariga bag'ishlangan. Bu boshlang'ich va o'rta darajadagi (A1-A2) o'quvchilar uchun fundamental mavzu hisoblanadi.\n\n**Murakkablik darajasi:**\nTest savollari asosan **"yodlash va qo'llash"** (recall and application) darajasida tuzilgan. Murakkablik darajasi past (Easy). O'quvchidan faqat gapning darak, inkor yoki so'roq shaklida ekanligini va otning sanaladigan/sanalmaydiganligini farqlash talab etiladi.\n\n**Test sifati va tavsiyalar:**\n*   **Ijobiy tomoni:** Test o'z oldiga qo'ygan maqsadga (some/any qoidalarini mustahkamlash) to'liq javob beradi. Savollar ketma-ketligi mantiqiy.\n*   **Kamchiligi:** Testda variantlar juda bir xil (bir xil tipdagi chalg'ituvchi variantlar). Masalan, 15 ta savolning deyarli barchasi bir xil qolipda. Bu o'quvchida zerikish uyg'otishi mumkin.\n*   **Tavsiya:** Kelgusida testlarni yanada boyitish uchun "contextual" (kontekstli) savollarni qo'shish kerak. Masalan, ikki kishi o'rtasidagi dialog ko'rinishidagi savollar o'quvchining amaliy ko'nikmasini yaxshiroq tekshiradi.\n\n---\n\n### 2. Savollar tahlili va to'g'ri javoblar\n\nQuyidagi jadvalda har bir savolning to'g'ri javobi va qisqacha izohi keltirilgan:\n\n| Savol № | To'g'ri javob | Izoh |\n| :--- | :--- | :--- |\n| 1 | **B) some** | Darak gap, sanalmaydigan ot. |\n| 2 | **A) any** | So'roq gap, sanaladigan ot. |\n| 3 | **C) some** | Darak gap, miqdor bildiradi. |\n| 4 | **B) any** | Inkor gap, sanaladigan ot. |\n| 5 | **C) some** | Darak gap, sanaladigan ot. |\n| 6 | **B) any** | So'roq gap (taklif bo'lmagan holat). |\n| 7 | **B) some** | Darak gap, sanalmaydigan ot. |\n| 8 | **A) any** | Inkor gap, sanalmaydigan ot. |\n| 9 | **C) some** | Darak gap, sanalmaydigan ot. |\n| 10 | **C) any** | So'roq gap, sanaladigan ot. |\n| 11 | **B) some** | Darak gap, sanaladigan ot. |\n| 12 | **B) any** | Inkor gap, sanaladigan ot. |\n| 13 | **A) some** | Taklif (Would you like...), istisno holat. |\n| 14 | **B) some** | Darak gap, sanalmaydigan ot. |\n| 15 | **C) any** | Inkor gap, sanalmaydigan ot. |\n\n---\n\n**Xulosa:** Ushbu test o'quvchilarning *some* va *any* qoidalarini o'zlashtirganligini tekshirish uchun juda samarali va aniq tuzilgan. Metodik jihatdan xatoliklar yo'q, javoblar kaliti to'g'ri belgilangan.	2026-06-11 18:10:25.499433+05	[{"id": 481, "question": "There is ____ water in the glass.", "options": {"A": "any", "B": "some", "C": "many", "D": "few"}, "correct": "B", "image_path": null}, {"id": 482, "question": "Are there ____ students in the room?", "options": {"A": "any", "B": "some", "C": "much", "D": "a lot"}, "correct": "A", "image_path": null}, {"id": 483, "question": "I have ____ money, but not enough.", "options": {"A": "any", "B": "no", "C": "some", "D": "many"}, "correct": "C", "image_path": null}, {"id": 484, "question": "He doesn't have ____ friends.", "options": {"A": "some", "B": "any", "C": "a lot", "D": "much"}, "correct": "B", "image_path": null}, {"id": 485, "question": "There are ____ apples on the table.", "options": {"A": "any", "B": "much", "C": "some", "D": "a"}, "correct": "C", "image_path": null}, {"id": 486, "question": "Do you need ____ help?", "options": {"A": "some", "B": "any", "C": "many", "D": "no"}, "correct": "B", "image_path": null}, {"id": 487, "question": "I need ____ information.", "options": {"A": "any", "B": "some", "C": "a", "D": "many"}, "correct": "B", "image_path": null}, {"id": 488, "question": "She didn't buy ____ bread.", "options": {"A": "any", "B": "some", "C": "a", "D": "many"}, "correct": "A", "image_path": null}, {"id": 489, "question": "There is ____ milk left.", "options": {"A": "any", "B": "many", "C": "some", "D": "few"}, "correct": "C", "image_path": null}, {"id": 490, "question": "Are there ____ chairs here?", "options": {"A": "some", "B": "much", "C": "any", "D": "a"}, "correct": "C", "image_path": null}, {"id": 491, "question": "He has ____ books.", "options": {"A": "any", "B": "some", "C": "much", "D": "no"}, "correct": "B", "image_path": null}, {"id": 492, "question": "I don't see ____ people.", "options": {"A": "some", "B": "any", "C": "a lot", "D": "much"}, "correct": "B", "image_path": null}, {"id": 493, "question": "Would you like ____ coffee?", "options": {"A": "some", "B": "any", "C": "many", "D": "few"}, "correct": "A", "image_path": null}, {"id": 494, "question": "I have ____ time.", "options": {"A": "any", "B": "some", "C": "many", "D": "no"}, "correct": "B", "image_path": null}, {"id": 495, "question": "There isn't ____ sugar.", "options": {"A": "some", "B": "many", "C": "any", "D": "few"}, "correct": "C", "image_path": null}]
27	\N	\N	Assalomu alaykum. Tajribali metodist sifatida taqdim etilgan test savollarini pedagogik va metodik nuqtai nazardan tahlil qildim. Quyida ushbu tahlil va savollarning to‘g‘ri javoblari keltirilgan.\n\n---\n\n### 1. Pedagogik va Metodik Tahlil\n\n**Mavzu qamrovi:**\nTest savollari ingliz tilida sonlarni (numerals) to‘g‘ri o‘qish va yozish ko‘nikmasini tekshirishga qaratilgan. Bu ingliz tili grammatikasining "Numbers" (sonlar) bo‘limi uchun juda mos va zaruriy mavzu hisoblanadi.\n\n**Murakkablik darajasi:**\n*   **Daraja:** O‘rta (Intermediate).\n*   **Tahlil:** Savollar oddiy birliklardan boshlanib, milliardlar guruhigacha bo‘lgan diapazonni qamrab olgan. Bu o‘quvchining sonlar tizimidagi "million" va "billion" kabi xalqaro raqamlar tizimini tushunish darajasini aniqlash uchun yetarli.\n\n**Variantlar sifati:**\n*   Variantlar "chalg‘ituvchi" (distractors) sifatida yaxshi tuzilgan. Masalan, 1-savolda "1,500,000" soni uchun "150,000" yoki "15,000,000" kabi variantlarning berilishi o‘quvchining xonalar (place value) bo‘yicha e’tiborli bo‘lishini talab qiladi.\n*   Variantlar mantiqiy ketma-ketlikda tuzilgan, bu esa testning sifatini oshiradi.\n\n**Umumiy xulosa:**\nTest o‘z maqsadiga to‘liq javob beradi. U o‘quvchining ingliz tilidagi sonlarni o‘qish qobiliyatini obyektiv baholashga xizmat qiladi. Savollar aniq va tushunarli tuzilgan.\n\n---\n\n### 2. Savollar va To‘g‘ri Javoblar tahlili\n\nQuyida har bir savolning to‘g‘ri javobi va qisqacha izohi keltirilgan:\n\n| Savol № | To‘g‘ri javob | Izoh |\n| :--- | :---: | :--- |\n| **1** | **A** | 1,500,000 = One million five hundred thousand. |\n| **2** | **B** | 25,750,000 = Twenty-five million seven hundred fifty thousand. |\n| **3** | **C** | 100,000,000 = One hundred million. |\n| **4** | **C** | 5,200,000,000 = Five billion two hundred million. |\n| **5** | **A** | 850,500 = Eight hundred fifty thousand five hundred. |\n\n---\n\n### Metodist tavsiyasi:\nTestni yanada boyitish uchun keyingi bosqichlarda **"ordinal numbers"** (tartib sonlar: *first, second, hundredth*) yoki **"decimal numbers"** (o‘nli kasrlar: *1.5, 2.75*) mavzularini ham qo‘shish maqsadga muvofiq bo‘ladi. Bu o‘quvchilarning sonlar bo‘yicha bilimini yanada chuqurlashtiradi.	2026-06-11 18:11:13.151688+05	[{"id": 496, "question": "1,500,000 sonining ingliz tilida to'g'ri o'qilishini tanlang.", "options": {"A": "One million five hundred thousand", "B": "One hundred fifty thousand", "C": "Fifteen million", "D": "One million five hundred"}, "correct": "A", "image_path": null}, {"id": 497, "question": "25,750,000 sonining ingliz tilida to'g'ri o'qilishini tanlang.", "options": {"A": "Two million five hundred seventy-five thousand", "B": "Twenty-five million seven hundred fifty thousand", "C": "Twenty-five thousand seven hundred fifty", "D": "Two hundred fifty-seven million five hundred thousand"}, "correct": "B", "image_path": null}, {"id": 498, "question": "100,000,000 sonining ingliz tilida to'g'ri o'qilishini tanlang.", "options": {"A": "Ten million", "B": "One billion", "C": "One hundred million", "D": "One hundred thousand"}, "correct": "C", "image_path": null}, {"id": 499, "question": "5,200,000,000 sonining ingliz tilida to'g'ri o'qilishini tanlang.", "options": {"A": "Five million two hundred thousand", "B": "Fifty-two billion", "C": "Five billion two hundred million", "D": "Five hundred twenty million"}, "correct": "C", "image_path": null}, {"id": 500, "question": "850,500 sonining ingliz tilida to'g'ri o'qilishini tanlang.", "options": {"A": "Eight hundred fifty thousand five hundred", "B": "Eighty-five thousand five hundred", "C": "Eight hundred fifty five hundred", "D": "Eight million fifty thousand five hundred"}, "correct": "A", "image_path": null}]
28	\N	\N	Assalomu alaykum! Tajribali metodist sifatida taqdim etilgan test savollarini pedagogik nuqtai nazardan tahlil qildim. Quyida ushbu tahlil va savollarning javoblari keltirilgan.\n\n---\n\n### 📋 Pedagogik tahlil\n\n**1. Mavzu qamrovi:**\nTest ingliz tili fanining "Reading Comprehension" (Matnni tushunish) bo'limiga tegishli. Unda oddiy hikoya asosida faktlarni aniqlash, detallarni ajratib olish va savol-javob ko'nikmalari tekshirilgan.\n\n**2. Murakkablik darajasi:**\nSavollar **"Beginner" (A1)** darajasiga mos keladi. Ular matndagi ma'lumotlarni to'g'ridan-to'g'ri topishga (literal comprehension) qaratilgan. Murakkab mantiqiy xulosalar talab qilinmagani uchun o'quvchilar uchun bajarish oson va tushunarli.\n\n**3. Variantlarning sifati:**\n*   **Distraktorlar (chalg'ituvchi variantlar):** Variantlar yaxshi tanlangan. Ular matndagi kontekstga mos keladigan, lekin noto'g'ri ma'lumotlarni o'z ichiga olgan. Bu o'quvchining diqqatini tekshirish uchun juda samarali.\n*   **Izchillik:** Barcha savollar bitta matn asosida tuzilgani o'quvchining matnni yaxlit tushunishini baholashga imkon beradi.\n\n**4. Umumiy xulosa:**\nTest o'z maqsadiga to'liq javob beradi. U boshlang'ich bosqichdagi o'quvchilar uchun juda mos. Savollar aniq, lo'nda va mantiqiy ketma-ketlikda tuzilgan.\n\n---\n\n### ✅ Savollar va to'g'ri javoblar\n\n| Savol № | Savol mazmuni | To'g'ri javob |\n| :--- | :--- | :--- |\n| **1** | Where does Sam live? | **B) In a big house** |\n| **2** | What does he drink? | **C) Coffee** |\n| **3** | How does he go to work? | **D) By bus** |\n| **4** | Why does he like his work? | **A) Because it is easy** |\n| **5** | Is his house small? | **B) No, it is big** |\n\n---\n\n**Metodist tavsiyasi:**\nAgar ushbu testni yanada boyitmoqchi bo'lsangiz, kelajakda matnga "Vocabulary" (so'z boyligi) yoki "Grammar" (masalan, Present Simple zamonini qo'llash) bo'yicha 1-2 ta qo'shimcha savol qo'shish orqali testning qamrovini kengaytirishingiz mumkin. Hozirgi holatida test o'z darajasi uchun **a'lo darajada** tuzilgan.	2026-06-11 18:11:48.411742+05	[{"id": 501, "question": "Read and answer: \\"My name is Sam. I live in a big house. Every morning, I drink coffee and eat bread. I go to work by bus. I like my work because it is easy.\\"<br/>Where does Sam live?", "options": {"A": "In a small house", "B": "In a big house", "C": "In an apartment", "D": "In the office"}, "correct": "B", "image_path": null}, {"id": 502, "question": "Read and answer: \\"My name is Sam. I live in a big house. Every morning, I drink coffee and eat bread. I go to work by bus. I like my work because it is easy.\\"<br/>What does he drink?", "options": {"A": "Tea", "B": "Milk", "C": "Coffee", "D": "Water"}, "correct": "C", "image_path": null}, {"id": 503, "question": "Read and answer: \\"My name is Sam. I live in a big house. Every morning, I drink coffee and eat bread. I go to work by bus. I like my work because it is easy.\\"<br/>How does he go to work?", "options": {"A": "By car", "B": "By train", "C": "On foot", "D": "By bus"}, "correct": "D", "image_path": null}, {"id": 504, "question": "Read and answer: \\"My name is Sam. I live in a big house. Every morning, I drink coffee and eat bread. I go to work by bus. I like my work because it is easy.\\"<br/>Why does he like his work?", "options": {"A": "Because it is easy", "B": "Because it pays well", "C": "Because he likes his colleagues", "D": "Because it is near his house"}, "correct": "A", "image_path": null}, {"id": 505, "question": "Read and answer: \\"My name is Sam. I live in a big house. Every morning, I drink coffee and eat bread. I go to work by bus. I like my work because it is easy.\\"<br/>Is his house small?", "options": {"A": "Yes, it is", "B": "No, it is big", "C": "No, he lives in a flat", "D": "He doesn't have a house"}, "correct": "B", "image_path": null}]
29	\N	\N	Assalomu alaykum! Tajribali metodist sifatida taqdim etilgan test savollarini tahlil qildim. Quyida ushbu testlar to‘plami bo‘yicha pedagogik xulosa va savollarning tahlili keltirilgan.\n\n---\n\n### 📋 Pedagogik tahlil va xulosa\n\n**1. Mavzu qamrovi:**\nTestlar to‘plami "Oddiy kasrlar ustida amallar" mavzusini to‘liq qamrab olgan. Unda quyidagi kichik mavzular ketma-ketlikda yoritilgan:\n*   Turli maxrajli kasrlarni qo‘shish va ayirish (1-7-savollar).\n*   Aralash sonlar ustida amallar (8-10-savollar).\n*   Amaliy (matnli) masalalar (11-15-savollar).\n\n**2. Murakkablik darajasi:**\nTestlar "osondan murakkabga" tamoyili asosida tuzilgan. Dastlabki savollar mexanik hisoblash ko‘nikmalarini tekshirsa, oxirgi savollar o‘quvchining mantiqiy fikrlash va matematik modellashtirish qobiliyatini baholaydi. Murakkablik darajasi o‘rta maktab o‘quvchilari (5-6-sinf) uchun juda mos keladi.\n\n**3. Test sifati va variantlar:**\n*   **Chalg‘ituvchi variantlar (distraktorlar):** Variantlar juda puxta o‘ylangan. Masalan, 1-savolda $1/2 + 1/3$ ni noto‘g‘ri qo‘shib $2/5$ (suratlarni va maxrajlarni alohida qo‘shish xatosi) deb belgilash ehtimoli hisobga olingan. Bu o‘quvchining tipik xatolarini aniqlashga yordam beradi.\n*   **Matnli masalalar:** 11-15-savollar o‘quvchining hayotiy vaziyatlarda kasrlardan foydalana olishini tekshiradi, bu esa kompetensiyaviy yondashuvga mos keladi.\n\n**4. Metodik tavsiya:**\nTestlar to‘plami sifatli. Faqat 1-savoldagi rasm (img tag) testning vizual qismini boyitgan, ammo matnli qismda "1/2 + 1/3" ifodasi aniq yozilgani uchun rasm shart emasdek ko‘rinadi. Umuman olganda, test o‘quvchilar bilimini xolisona baholash uchun juda mos.\n\n---\n\n### ✅ Savollar va to‘g‘ri javoblar tahlili\n\n| Savol № | To‘g‘ri javob | Izoh / Hisoblash |\n| :--- | :--- | :--- |\n| 1 | **B** | $3/6 + 2/6 = 5/6$ |\n| 2 | **A** | $3/4 - 2/4 = 1/4$ |\n| 3 | **B** | $4/10 + 3/10 = 7/10$ |\n| 4 | **B** | $5/6 - 2/6 = 3/6 = 1/2$ |\n| 5 | **B** | $8/12 + 3/12 = 11/12$ |\n| 6 | **C** | $35/40 - 16/40 = 19/40$ |\n| 7 | **A** | $6/6 - 4/6 - 1/6 = 1/6$ |\n| 8 | **B** | $2 2/4 + 1 1/4 = 3 3/4$ |\n| 9 | **A** | $3 4/6 - 1 3/6 = 2 1/6$ |\n| 10 | **B** | $4 2/10 - 2 5/10 = 3 12/10 - 2 5/10 = 1 7/10$ |\n| 11 | **A** | $3/4 + 2/4 = 5/4 = 1 1/4$ |\n| 12 | **B** | $2 2/4 - 3/4 = 1 6/4 - 3/4 = 1 3/4$ |\n| 13 | **B** | $5/15 + 6/15 = 11/15$ |\n| 14 | **C** | $5/8 - 2/8 = 3/8$ |\n| 15 | **A** | $1/2 + (1/2 + 1/5) + 3/10 = 5/10 + 7/10 + 3/10 = 15/10 = 1 1/2$ |\n\nUshbu tahlil o‘quv jarayonida o‘quvchilarning o‘zlashtirish darajasini aniqlashda samarali vosita bo‘lib xizmat qiladi.	2026-06-20 21:53:11.327195+05	[{"id": 534, "question": "Hisoblang: 1/2 + 1/3 <br><img src=\\"/static/uploads/quiz_images/e4e07d5c-724e-4ccf-bfe2-24f59c32aedd.jpeg\\" class=\\"quiz-inline-img\\" alt=\\"Test Rasm\\"><br>", "options": {"A": "2/5", "B": "5/6", "C": "2/3", "D": "1/6"}, "correct": "B", "image_path": null}, {"id": 535, "question": "Hisoblang: 3/4 - 1/2", "options": {"A": "1/4", "B": "2/2", "C": "1/2", "D": "1/8"}, "correct": "A", "image_path": null}, {"id": 536, "question": "Amalni bajaring: 2/5 + 3/10", "options": {"A": "5/15", "B": "7/10", "C": "1/2", "D": "4/5"}, "correct": "B", "image_path": null}, {"id": 537, "question": "Hisoblang: 5/6 - 1/3", "options": {"A": "4/3", "B": "1/2", "C": "2/3", "D": "4/6"}, "correct": "B", "image_path": null}, {"id": 538, "question": "Yig‘indini toping: 2/3 + 1/4", "options": {"A": "3/7", "B": "11/12", "C": "7/12", "D": "5/12"}, "correct": "B", "image_path": null}, {"id": 539, "question": "Ayirmani hisoblang: 7/8 - 2/5", "options": {"A": "5/3", "B": "9/40", "C": "19/40", "D": "5/40"}, "correct": "C", "image_path": null}, {"id": 540, "question": "Hisoblang: 1 - 2/3 - 1/6", "options": {"A": "1/6", "B": "1/3", "C": "1/2", "D": "5/6"}, "correct": "A", "image_path": null}, {"id": 541, "question": "Hisoblang: 2 1/2 + 1 1/4", "options": {"A": "3 2/6", "B": "3 3/4", "C": "3 1/2", "D": "4 1/4"}, "correct": "B", "image_path": null}, {"id": 542, "question": "Ayirmani toping: 3 2/3 - 1 1/2", "options": {"A": "2 1/6", "B": "2 1/1", "C": "1 5/6", "D": "2 1/3"}, "correct": "A", "image_path": null}, {"id": 543, "question": "Hisoblang: 4 1/5 - 2 1/2", "options": {"A": "2 3/10", "B": "1 7/10", "C": "2 1/3", "D": "1 3/10"}, "correct": "B", "image_path": null}, {"id": 544, "question": "Madina do‘kondan 3/4 kg olma va 1/2 kg banan sotib oldi. U jami necha kilogramm meva sotib olgan?", "options": {"A": "1 1/4 kg", "B": "4/6 kg", "C": "1 1/2 kg", "D": "3/8 kg"}, "correct": "A", "image_path": null}, {"id": 545, "question": "Idishda 2 1/2 litr sut bor edi. Undan pirog pishirish uchun 3/4 litr sut ishlatildi. Idishda qancha sut qoldi?", "options": {"A": "1 1/2 litr", "B": "1 3/4 litr", "C": "2 1/4 litr", "D": "1 1/4 litr"}, "correct": "B", "image_path": null}, {"id": 546, "question": "Sayyoh birinchi soatda yo‘lning 1/3 qismini, ikkinchi soatda esa 2/5 qismini bosib o‘tdi. U ikki soatda yo‘lning qancha qismini bosib o‘tgan?", "options": {"A": "3/8 qismini", "B": "11/15 qismini", "C": "2/15 qismini", "D": "4/5 qismini"}, "correct": "B", "image_path": null}, {"id": 547, "question": "Hovuzdagi suvning 5/8 qismi to‘ldirilgan. Quyosh issig‘ida suvning 1/4 qismi bug‘lanib ketdi. Hovuzning qancha qismida suv qoldi?", "options": {"A": "4/4 qismi", "B": "1/2 qismi", "C": "3/8 qismi", "D": "1/8 qismi"}, "correct": "C", "image_path": null}, {"id": 548, "question": "Uchburchakning birinchi tomoni 1/2 m, ikkinchi tomoni birinchisidan 1/5 m uzun, uchinchi tomoni esa 3/10 m. Uchburchakning perimetrini toping.", "options": {"A": "1 1/2 m", "B": "1 m", "C": "1 2/5 m", "D": "9/10 m"}, "correct": "A", "image_path": null}]
\.


--
-- TOC entry 5113 (class 0 OID 16423)
-- Dependencies: 220
-- Data for Name: promo_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.promo_codes (id, code, discount_percent, max_uses, used_count, is_active, expires_at) FROM stdin;
\.


--
-- TOC entry 5121 (class 0 OID 16501)
-- Dependencies: 228
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, test_id, question_text, option_a, option_b, option_c, option_d, correct_answer) FROM stdin;
\.


--
-- TOC entry 5115 (class 0 OID 16437)
-- Dependencies: 222
-- Data for Name: referrals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.referrals (id, user_id, by_user_id, created_at, bonus_amount) FROM stdin;
\.


--
-- TOC entry 5145 (class 0 OID 41258)
-- Dependencies: 252
-- Data for Name: scoin_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scoin_history (id, user_id, amount, description, created_at) FROM stdin;
61	13	-1000	Background sotib olindi: SStudio logo	2026-06-20 21:51:11.333544+05
62	13	-100	Color sotib olindi: Pushti	2026-06-20 21:51:32.780889+05
63	13	0	Background sotib olindi: Odatiy	2026-06-20 21:51:59.675047+05
64	14	-1000	Background sotib olindi: SStudio logo	2026-06-20 21:52:12.875099+05
66	14	0	Background sotib olindi: Odatiy	2026-06-20 21:52:31.155796+05
67	14	-1000	Background sotib olindi: SStudio logo	2026-06-20 21:52:33.57243+05
118	6	-230	Animation sotib olindi: Runner	2026-06-21 18:52:04.486826+05
119	6	-230	Animation sotib olindi: Runner	2026-06-21 18:53:30.743894+05
120	6	-230	Animation sotib olindi: Runner	2026-06-21 18:54:47.331909+05
121	6	-230	Animation sotib olindi: Runner	2026-06-21 18:57:13.335934+05
122	6	-430	Animation sotib olindi: Runner	2026-06-21 18:58:53.262567+05
123	6	-10000	Rank sotib olindi: Legandary	2026-06-21 19:22:52.488562+05
124	6	-800	Animation sotib olindi: Kamalak Hoshiya	2026-06-21 19:23:25.951176+05
125	6	-1500	Animation sotib olindi: Kamalak Hoshiya + Runner	2026-06-21 19:24:45.022812+05
126	6	-1500	Animation sotib olindi: Rainbow Runner	2026-06-21 19:27:00.709792+05
127	6	-1500	Animation sotib olindi: Rainbow Runner	2026-06-21 19:27:03.035066+05
\.


--
-- TOC entry 5137 (class 0 OID 41208)
-- Dependencies: 244
-- Data for Name: shop_animations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_animations (id, name, description, price, css_code, is_active) FROM stdin;
2	Lazer		150	.user-card {\r\n    position: relative;\r\n    overflow: hidden;\r\n    /* Karta uchun asosiy stil */\r\n    border: 2px solid rgba(255, 255, 255, 0.1);\r\n    background: #1a1a1a; \r\n}\r\n\r\n/* Skaner chizig'i */\r\n.user-card::after {\r\n    content: '';\r\n    position: absolute;\r\n    top: 0;\r\n    left: -100%;\r\n    width: 100%;\r\n    height: 100%;\r\n    background: linear-gradient(\r\n        90deg, \r\n        transparent, \r\n        rgba(0, 242, 254, 0.3), \r\n        transparent\r\n    );\r\n    animation: scanner 3s infinite linear;\r\n    pointer-events: none;\r\n}\r\n\r\n@keyframes scanner {\r\n    0% { left: -100%; }\r\n    100% { left: 100%; }\r\n}	t
3	Nafas olish		120	.user-card {\r\n    border: 2px solid rgba(0, 255, 255, 0.5) !important;\r\n    animation: neon-pulse 2s infinite ease-in-out;\r\n}\r\n@keyframes neon-pulse {\r\n    0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }\r\n    50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.6); }\r\n    100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }\r\n}	t
6	Aylanma oltin		400	.user-card {\r\n    position: relative;\r\n    overflow: hidden;\r\n}\r\n.user-card::after {\r\n    content: '';\r\n    position: absolute;\r\n    top: -50%; left: -50%;\r\n    width: 200%; height: 200%;\r\n    background: linear-gradient(45deg, transparent, rgba(255, 215, 0, 0.3), transparent);\r\n    animation: gold-shine 4s infinite linear;\r\n}\r\n@keyframes gold-shine {\r\n    0% { transform: rotate(0deg); }\r\n    100% { transform: rotate(360deg); }\r\n}	t
37	Kamalak Hoshiya		800	.user-card {\r\n    border: 2px solid transparent !important;\r\n    background-clip: padding-box, border-box;\r\n    background-origin: padding-box, border-box;\r\n    background-image: linear-gradient(to right, #1a1a1a, #1a1a1a), \r\n                      linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);\r\n    animation: rainbow 5s infinite linear;\r\n}\r\n@keyframes rainbow {\r\n    0% { filter: hue-rotate(0deg); }\r\n    100% { filter: hue-rotate(360deg); }\r\n}	t
42	Runner		430	.user-card {\r\n    position: relative;\r\n    /* 5 soniyalik animatsiya, cubic-bezier o'rtada sekinlashishni ta'minlaydi */\r\n    animation: fullRunner 5s cubic-bezier(0.4, 0, 0.2, 1) infinite;\r\n}\r\n\r\n@keyframes fullRunner {\r\n    0% { \r\n        transform: translateX(-100vw); \r\n    }\r\n    50% { \r\n        /* O'rtaga kelganda - bu yerda sekinlik darajasini sozlash mumkin */\r\n        transform: translateX(0); \r\n    }\r\n    100% { \r\n        transform: translateX(100vw); \r\n    }\r\n}\r\n.user-card {\r\n    /* Animatsiya uchun transition qoidasi */\r\n    transition: transform 0.8s ease-out;\r\n    animation: fullRunner 5s cubic-bezier(0.4, 0, 0.2, 1) infinite;\r\n}\r\n\r\n/* Sichqonchani olib kelganda sekin to'xtashi uchun */\r\n.user-card:hover {\r\n    animation-play-state: paused;\r\n    transition: animation-play-state 0.5s ease-out;\r\n}	t
44	Rainbow Runner		1500	.user-card {\r\n    position: relative;\r\n    \r\n    /* Rainbow (Kamalak) border effektlari */\r\n    border: 2px solid transparent !important;\r\n    background-clip: padding-box, border-box;\r\n    background-origin: padding-box, border-box;\r\n    background-image: linear-gradient(to right, #1a1a1a, #1a1a1a), \r\n                      linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);\r\n    \r\n    /* 🔥 MUHIM: Ikkala animatsiyani vergul bilan ajratib bitta qatorga yozamiz */\r\n    animation: fullRunner 5s cubic-bezier(0.4, 0, 0.2, 1) infinite, \r\n               rainbow 5s infinite linear;\r\n}\r\n\r\n/* Sichqoncha kelganda har ikkala animatsiya ham joyida taqqa to'xtaydi */\r\n.user-card:hover {\r\n    animation-play-state: paused;\r\n}\r\n\r\n/* 1-Animatsiya: Chapdan o'ngga uchib o'tish */\r\n@keyframes fullRunner {\r\n    0% { transform: translateX(-100vw); }\r\n    50% { transform: translateX(0); } /* Ekranning o'rtasida cubic-bezier hisobiga sekinlashadi */\r\n    100% { transform: translateX(100vw); }\r\n}\r\n\r\n/* 2-Animatsiya: Border rangini aylantirish */\r\n@keyframes rainbow {\r\n    0% { filter: hue-rotate(0deg); }\r\n    100% { filter: hue-rotate(360deg); }\r\n}	t
\.


--
-- TOC entry 5141 (class 0 OID 41230)
-- Dependencies: 248
-- Data for Name: shop_backgrounds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_backgrounds (id, name, description, price, picture, is_active) FROM stdin;
1	SStudio logo	SSTudioni ikonka belgisini orqa fon sifatida joylashtirish	1000	/static/icon/dark_icon.png	t
2	Odatiy	SStudioni Standart orqa foni	0	/static/images/default_bg.png	t
8	Cyber City		670	/uploads/image.png	t
\.


--
-- TOC entry 5139 (class 0 OID 41219)
-- Dependencies: 246
-- Data for Name: shop_colors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_colors (id, name, description, price, color, is_active) FROM stdin;
2	Pushti		100	#ff00ff	t
4	Ochiq moviy 		60	#00ffff	t
5	Sariq 		90	#ffff00	t
6	Oq		20	#ffffff	t
7	Qizil 		250	#ff0000	t
8	Qorovul koʻk		150	#0000ff	t
\.


--
-- TOC entry 5143 (class 0 OID 41241)
-- Dependencies: 250
-- Data for Name: shop_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_history (id, user_id, item_type, item_id, item_name, price, details, created_at) FROM stdin;
\.


--
-- TOC entry 5135 (class 0 OID 41197)
-- Dependencies: 242
-- Data for Name: shop_ranks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shop_ranks (id, name, description, price, picture, name_color, rank_color, is_active) FROM stdin;
1	defualt		20	\N	\N	#ffffff	t
16	epic		3200	\N	\N	#ff1ab6	t
17	common		500	\N	\N	#82df43	t
18	Uncommon		700	\N	\N	#649da0	t
19	Rare		1020	\N	\N	#02d8e3	t
20	Teacher		1500	\N	\N	#a42361	t
21	Pupil		900	\N	\N	#c8ab1e	t
22	EXport		1700	\N	\N	#1f00bd	t
23	Legandary		10000	\N	\N	#fafe20	t
\.


--
-- TOC entry 5127 (class 0 OID 32893)
-- Dependencies: 234
-- Data for Name: telegram_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telegram_accounts (id, user_id, tg_id, username, first_name, last_name, is_active, created_at) FROM stdin;
1	6	997572546	dilafruz_198619	Sardor	\N	t	2026-06-04 14:37:57.946411+05
3	9	2089398711	J88M94A15J20J22	Muxlisa Raimovaa	\N	t	2026-06-06 21:54:10.233272+05
5	12	997572546	dilafruz_198619	Sardor	\N	t	2026-06-20 21:41:52.820256+05
6	13	1323217434	fcluz	Abdurahim	\N	t	2026-06-20 21:44:10.797896+05
\.


--
-- TOC entry 5131 (class 0 OID 32969)
-- Dependencies: 238
-- Data for Name: test_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_results (id, user_id, test_id, correct_answers, total_questions, percentage, created_at) FROM stdin;
1	6	29	2	15	13.333333333333334	2026-06-06 10:39:44.458445+05
2	6	30	3	15	20	2026-06-06 11:35:18.974887+05
3	9	31	25	30	83.33333333333334	2026-06-06 22:28:48.931965+05
4	6	31	30	30	100	2026-06-06 22:28:48.931965+05
12	9	32	19	20	95	2026-06-07 22:36:15.947584+05
13	6	32	6	20	30	2026-06-07 22:36:15.947584+05
14	9	33	18	20	90	2026-06-11 18:05:22.671993+05
16	9	34	10	10	100	2026-06-11 18:07:34.733136+05
20	9	36	9	20	45	2026-06-11 18:09:42.678698+05
22	9	37	15	15	100	2026-06-11 18:10:25.499433+05
24	9	38	5	5	100	2026-06-11 18:11:13.151688+05
26	9	39	5	5	100	2026-06-11 18:11:48.411742+05
27	6	40	1	15	6.666666666666667	2026-06-20 21:53:11.327195+05
28	13	40	6	15	40	2026-06-20 21:53:11.327195+05
\.


--
-- TOC entry 5119 (class 0 OID 16488)
-- Dependencies: 226
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tests (id, title, created_at, user_id, description, is_public, status) FROM stdin;
\.


--
-- TOC entry 5123 (class 0 OID 32863)
-- Dependencies: 230
-- Data for Name: user_allowed_tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_allowed_tests (id, user_id, test_id, allowed_at) FROM stdin;
1	6	1	2026-06-02 18:01:57.611659
2	6	12	2026-06-02 19:42:02.052853
3	6	22	2026-06-03 10:05:33.106837
4	6	26	2026-06-06 09:13:31.041007
5	8	26	2026-06-06 09:24:57.489877
6	9	31	2026-06-06 21:55:20.558879
7	10	31	2026-06-06 22:05:45.817727
8	6	31	2026-06-06 22:13:41.302511
9	10	32	2026-06-07 21:25:08.772349
10	9	32	2026-06-07 21:30:57.312015
11	6	32	2026-06-07 21:32:14.59965
12	9	33	2026-06-11 09:40:04.668716
13	10	33	2026-06-11 09:40:19.53333
14	6	40	2026-06-20 21:45:35.391069
15	13	40	2026-06-20 21:45:43.835631
\.


--
-- TOC entry 5125 (class 0 OID 32872)
-- Dependencies: 232
-- Data for Name: user_options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_options (id, test_id, user_id, options, "end") FROM stdin;
\.


--
-- TOC entry 5133 (class 0 OID 41181)
-- Dependencies: 240
-- Data for Name: user_statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_statuses (id, user_id, rank, picture, animation, color, name_color, rank_color, css_code) FROM stdin;
2	13		\N			\N	\N	\N
3	14		\N			\N	\N	\N
1	6	Legandary	\N	.user-card {\r\n    position: relative;\r\n    \r\n    /* Rainbow (Kamalak) border effektlari */\r\n    border: 2px solid transparent !important;\r\n    background-clip: padding-box, border-box;\r\n    background-origin: padding-box, border-box;\r\n    background-image: linear-gradient(to right, #1a1a1a, #1a1a1a), \r\n                      linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);\r\n    \r\n    /* 🔥 MUHIM: Ikkala animatsiyani vergul bilan ajratib bitta qatorga yozamiz */\r\n    animation: fullRunner 5s cubic-bezier(0.4, 0, 0.2, 1) infinite, \r\n               rainbow 5s infinite linear;\r\n}\r\n\r\n/* Sichqoncha kelganda har ikkala animatsiya ham joyida taqqa to'xtaydi */\r\n.user-card:hover {\r\n    animation-play-state: paused;\r\n}\r\n\r\n/* 1-Animatsiya: Chapdan o'ngga uchib o'tish */\r\n@keyframes fullRunner {\r\n    0% { transform: translateX(-100vw); }\r\n    50% { transform: translateX(0); } /* Ekranning o'rtasida cubic-bezier hisobiga sekinlashadi */\r\n    100% { transform: translateX(100vw); }\r\n}\r\n\r\n/* 2-Animatsiya: Border rangini aylantirish */\r\n@keyframes rainbow {\r\n    0% { filter: hue-rotate(0deg); }\r\n    100% { filter: hue-rotate(360deg); }\r\n}	#ffff00	\N	#fafe20	\N
\.


--
-- TOC entry 5117 (class 0 OID 16458)
-- Dependencies: 224
-- Data for Name: user_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_tokens (id, token, user_id, ip_address, created_at) FROM stdin;
98	9d60b7a0-9e5c-42f6-808f-9d9d2626d767	6	127.0.0.1	2026-06-21 11:15:00.880984+05
99	eb8089de-616e-42ae-9495-be4b36ce5e01	16	127.0.0.1	2026-06-21 11:51:46.323779+05
100	2319123b-d29f-40ad-9e51-7c1c0b13fbda	6	127.0.0.1	2026-06-21 18:44:37.197139+05
\.


--
-- TOC entry 5111 (class 0 OID 16388)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, language, theme, scoin, xp, created_at, background, promo) FROM stdin;
6	sardor	$2b$12$ejF/na5o.mNCLUF83pXdNOx2t8cvBJOYPeTSMaXSsZG3knnBHKnV2	uz	light	767640	0	2026-05-29 11:00:33.236153+05	/uploads/image.png	sstudio-sardor-admin-pro
14	Husan	$2b$12$orHwrH7c1Gozn7XKPQOsvu1UDw5Yg31iRFXKgw6qQfxZWFKwACEeO	uz	dark	8000	0	2026-06-20 21:49:21.618579+05	/static/icon/dark_icon.png	
15	Aaaaa	$2b$12$EQwUeiiCckWn1clHgfXdtuRanKkwwFZsQua/yYjypAmKm3SkKVbJq	uz	dark	0	0	2026-06-20 21:55:14.651095+05	/static/images/default_bg.png	No
9	aziza	$2b$12$JN4iZPW6erb7owkOCGHAy.5PJgtn1buin190b3evm8DIXOAz8yS/G	uz	dark	0	0	2026-06-06 21:12:26.226016+05	/static/images/default_bg.png	No
12	Durdona	$2b$12$BYksQHP3poNjmeYEvGRDHu.31EjVVGpXLRQ5P9VLkFuU/6aAQ7MrO	uz	dark	0	0	2026-06-20 21:06:24.400193+05	/static/images/default_bg.png	
16	Sabrina_2015	$2b$12$/o0a.DmKwHhiiYfzyxLE8.VWa7VtlnVNO0kvFIxio2AEUnso8TGFi	uz	dark	0	0	2026-06-21 11:51:36.635213+05	/static/images/default_bg.png	No
13	Abdurahim	$2b$12$Mbw7QgEciKVjxCnWdYapNOA8MFdcVfbe4/K/xT3NQgbS95qxwv7qS	uz	dark	8900	0	2026-06-20 21:42:29.478338+05	/static/images/default_bg.png	IIIIIII
\.


--
-- TOC entry 5172 (class 0 OID 0)
-- Dependencies: 253
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_id_seq', 3, true);


--
-- TOC entry 5173 (class 0 OID 0)
-- Dependencies: 235
-- Name: ai_learning_analysis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_learning_analysis_id_seq', 29, true);


--
-- TOC entry 5174 (class 0 OID 0)
-- Dependencies: 219
-- Name: promo_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.promo_codes_id_seq', 1, false);


--
-- TOC entry 5175 (class 0 OID 0)
-- Dependencies: 227
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 548, true);


--
-- TOC entry 5176 (class 0 OID 0)
-- Dependencies: 221
-- Name: referrals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.referrals_id_seq', 1, false);


--
-- TOC entry 5177 (class 0 OID 0)
-- Dependencies: 251
-- Name: scoin_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.scoin_history_id_seq', 127, true);


--
-- TOC entry 5178 (class 0 OID 0)
-- Dependencies: 243
-- Name: shop_animations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_animations_id_seq', 44, true);


--
-- TOC entry 5179 (class 0 OID 0)
-- Dependencies: 247
-- Name: shop_backgrounds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_backgrounds_id_seq', 8, true);


--
-- TOC entry 5180 (class 0 OID 0)
-- Dependencies: 245
-- Name: shop_colors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_colors_id_seq', 8, true);


--
-- TOC entry 5181 (class 0 OID 0)
-- Dependencies: 249
-- Name: shop_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_history_id_seq', 1, false);


--
-- TOC entry 5182 (class 0 OID 0)
-- Dependencies: 241
-- Name: shop_ranks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shop_ranks_id_seq', 23, true);


--
-- TOC entry 5183 (class 0 OID 0)
-- Dependencies: 233
-- Name: telegram_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.telegram_accounts_id_seq', 6, true);


--
-- TOC entry 5184 (class 0 OID 0)
-- Dependencies: 237
-- Name: test_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_results_id_seq', 28, true);


--
-- TOC entry 5185 (class 0 OID 0)
-- Dependencies: 225
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tests_id_seq', 40, true);


--
-- TOC entry 5186 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_allowed_tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_allowed_tests_id_seq', 15, true);


--
-- TOC entry 5187 (class 0 OID 0)
-- Dependencies: 231
-- Name: user_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_options_id_seq', 33, true);


--
-- TOC entry 5188 (class 0 OID 0)
-- Dependencies: 239
-- Name: user_statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_statuses_id_seq', 3, true);


--
-- TOC entry 5189 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_tokens_id_seq', 100, true);


--
-- TOC entry 5190 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 16, true);


--
-- TOC entry 4946 (class 2606 OID 49385)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- TOC entry 4948 (class 2606 OID 49387)
-- Name: admins admins_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_user_id_key UNIQUE (user_id);


--
-- TOC entry 4920 (class 2606 OID 32937)
-- Name: ai_learning_analysis ai_learning_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_learning_analysis
    ADD CONSTRAINT ai_learning_analysis_pkey PRIMARY KEY (id);


--
-- TOC entry 4892 (class 2606 OID 16434)
-- Name: promo_codes promo_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promo_codes
    ADD CONSTRAINT promo_codes_code_key UNIQUE (code);


--
-- TOC entry 4894 (class 2606 OID 16432)
-- Name: promo_codes promo_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promo_codes
    ADD CONSTRAINT promo_codes_pkey PRIMARY KEY (id);


--
-- TOC entry 4909 (class 2606 OID 16508)
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- TOC entry 4898 (class 2606 OID 16444)
-- Name: referrals referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (id);


--
-- TOC entry 4944 (class 2606 OID 41264)
-- Name: scoin_history scoin_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scoin_history
    ADD CONSTRAINT scoin_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4933 (class 2606 OID 41217)
-- Name: shop_animations shop_animations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_animations
    ADD CONSTRAINT shop_animations_pkey PRIMARY KEY (id);


--
-- TOC entry 4937 (class 2606 OID 41239)
-- Name: shop_backgrounds shop_backgrounds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_backgrounds
    ADD CONSTRAINT shop_backgrounds_pkey PRIMARY KEY (id);


--
-- TOC entry 4935 (class 2606 OID 41228)
-- Name: shop_colors shop_colors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_colors
    ADD CONSTRAINT shop_colors_pkey PRIMARY KEY (id);


--
-- TOC entry 4941 (class 2606 OID 41249)
-- Name: shop_history shop_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_history
    ADD CONSTRAINT shop_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4931 (class 2606 OID 41206)
-- Name: shop_ranks shop_ranks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_ranks
    ADD CONSTRAINT shop_ranks_pkey PRIMARY KEY (id);


--
-- TOC entry 4918 (class 2606 OID 32902)
-- Name: telegram_accounts telegram_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telegram_accounts
    ADD CONSTRAINT telegram_accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 4925 (class 2606 OID 32975)
-- Name: test_results test_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_pkey PRIMARY KEY (id);


--
-- TOC entry 4907 (class 2606 OID 16494)
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- TOC entry 4912 (class 2606 OID 32869)
-- Name: user_allowed_tests user_allowed_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_allowed_tests
    ADD CONSTRAINT user_allowed_tests_pkey PRIMARY KEY (id);


--
-- TOC entry 4914 (class 2606 OID 32881)
-- Name: user_options user_options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_options
    ADD CONSTRAINT user_options_pkey PRIMARY KEY (id);


--
-- TOC entry 4927 (class 2606 OID 41188)
-- Name: user_statuses user_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_statuses
    ADD CONSTRAINT user_statuses_pkey PRIMARY KEY (id);


--
-- TOC entry 4929 (class 2606 OID 41190)
-- Name: user_statuses user_statuses_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_statuses
    ADD CONSTRAINT user_statuses_user_id_key UNIQUE (user_id);


--
-- TOC entry 4903 (class 2606 OID 16464)
-- Name: user_tokens user_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tokens
    ADD CONSTRAINT user_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 4905 (class 2606 OID 16466)
-- Name: user_tokens user_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tokens
    ADD CONSTRAINT user_tokens_token_key UNIQUE (token);


--
-- TOC entry 4887 (class 2606 OID 16400)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4889 (class 2606 OID 16402)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4949 (class 1259 OID 49393)
-- Name: idx_admin_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_admin_user_id ON public.admins USING btree (user_id);


--
-- TOC entry 4895 (class 1259 OID 16456)
-- Name: idx_by_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_by_user_id ON public.referrals USING btree (by_user_id);


--
-- TOC entry 4890 (class 1259 OID 16435)
-- Name: idx_promo_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_promo_code ON public.promo_codes USING btree (code);


--
-- TOC entry 4942 (class 1259 OID 41270)
-- Name: idx_scoin_history_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_scoin_history_user_id ON public.scoin_history USING btree (user_id);


--
-- TOC entry 4938 (class 1259 OID 41256)
-- Name: idx_shop_history_item_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shop_history_item_type_id ON public.shop_history USING btree (item_type, item_id);


--
-- TOC entry 4939 (class 1259 OID 41255)
-- Name: idx_shop_history_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shop_history_user_id ON public.shop_history USING btree (user_id);


--
-- TOC entry 4910 (class 1259 OID 32870)
-- Name: idx_user_allowed_tests_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_allowed_tests_user ON public.user_allowed_tests USING btree (user_id);


--
-- TOC entry 4896 (class 1259 OID 16455)
-- Name: idx_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_id ON public.referrals USING btree (user_id);


--
-- TOC entry 4885 (class 1259 OID 16405)
-- Name: idx_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_id ON public.users USING btree (id);


--
-- TOC entry 4915 (class 1259 OID 32908)
-- Name: ix_telegram_accounts_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_telegram_accounts_id ON public.telegram_accounts USING btree (id);


--
-- TOC entry 4916 (class 1259 OID 32909)
-- Name: ix_telegram_accounts_tg_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_telegram_accounts_tg_id ON public.telegram_accounts USING btree (tg_id);


--
-- TOC entry 4921 (class 1259 OID 32981)
-- Name: ix_test_results_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_test_results_id ON public.test_results USING btree (id);


--
-- TOC entry 4922 (class 1259 OID 32982)
-- Name: ix_test_results_test_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_test_results_test_id ON public.test_results USING btree (test_id);


--
-- TOC entry 4923 (class 1259 OID 32983)
-- Name: ix_test_results_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_test_results_user_id ON public.test_results USING btree (user_id);


--
-- TOC entry 4899 (class 1259 OID 16472)
-- Name: ix_user_tokens_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_tokens_id ON public.user_tokens USING btree (id);


--
-- TOC entry 4900 (class 1259 OID 16474)
-- Name: ix_user_tokens_ip_address; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_tokens_ip_address ON public.user_tokens USING btree (ip_address);


--
-- TOC entry 4901 (class 1259 OID 16473)
-- Name: ix_user_tokens_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_tokens_token ON public.user_tokens USING btree (token);


--
-- TOC entry 4958 (class 2606 OID 32959)
-- Name: ai_learning_analysis ai_learning_analysis_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_learning_analysis
    ADD CONSTRAINT ai_learning_analysis_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE SET NULL;


--
-- TOC entry 4959 (class 2606 OID 32943)
-- Name: ai_learning_analysis ai_learning_analysis_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_learning_analysis
    ADD CONSTRAINT ai_learning_analysis_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4963 (class 2606 OID 41265)
-- Name: scoin_history fk_scoin_history_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scoin_history
    ADD CONSTRAINT fk_scoin_history_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4962 (class 2606 OID 41250)
-- Name: shop_history fk_shop_history_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shop_history
    ADD CONSTRAINT fk_shop_history_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4957 (class 2606 OID 32903)
-- Name: telegram_accounts fk_telegram_accounts_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telegram_accounts
    ADD CONSTRAINT fk_telegram_accounts_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4955 (class 2606 OID 32882)
-- Name: user_options fk_test; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_options
    ADD CONSTRAINT fk_test FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- TOC entry 4960 (class 2606 OID 32976)
-- Name: test_results fk_test_results_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT fk_test_results_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4964 (class 2606 OID 49388)
-- Name: admins fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4956 (class 2606 OID 32887)
-- Name: user_options fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_options
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4961 (class 2606 OID 41191)
-- Name: user_statuses fk_user_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_statuses
    ADD CONSTRAINT fk_user_status FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4952 (class 2606 OID 16467)
-- Name: user_tokens fk_user_tokens_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tokens
    ADD CONSTRAINT fk_user_tokens_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4954 (class 2606 OID 16509)
-- Name: questions questions_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- TOC entry 4950 (class 2606 OID 16450)
-- Name: referrals referrals_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_by_user_id_fkey FOREIGN KEY (by_user_id) REFERENCES public.users(id);


--
-- TOC entry 4951 (class 2606 OID 16445)
-- Name: referrals referrals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4953 (class 2606 OID 16495)
-- Name: tests tests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2026-06-23 21:09:56

--
-- PostgreSQL database dump complete
--

\unrestrict vpIAgPnahwrWWkNxfzFhxOJ6cnV84pzYlWFZQwhKdpMqVclHODkHkvEV0nTmygp

-- Completed on 2026-06-23 21:09:56

--
-- PostgreSQL database cluster dump complete
--

