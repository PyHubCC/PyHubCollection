--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- Data for Name: topics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY topics (topic_id, name, slug, views, issues, followers) FROM stdin;
1	基础知识	basic	1	0	1
3	网站开发	web-dev	1	0	1
2	机器学习	ml	1	0	1
4	数据挖掘	data-mining	1	0	1
5	第三方库	3p-library	1	0	1
6	图像处理	image-proc	1	0	1
7	工具资源	tools	1	0	1
8	爬虫技术	spider-tech	1	0	1
\.


--
-- Name: topics_topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('topics_topic_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

