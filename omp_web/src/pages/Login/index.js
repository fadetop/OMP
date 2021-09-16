import { Input, Checkbox, Button, Form, message } from "antd";
import { useState } from "react";
import styles from "./index.module.less";
import img from "@/config/logo/logo.svg";
import {
  LockOutlined,
  UserOutlined,
  CloseCircleFilled,
} from "@ant-design/icons";
import { OmpContentWrapper } from "@/components";
import { fetchGet, fetchPost } from "@/utils/request";
import { apiRequest } from "@/config/requestApi";
import { handleResponse } from "@/utils/utils";
import { withRouter } from "react-router";

const Login = withRouter(({ history }) => {
  const [msgShow, setMsgShow] = useState(false);
  const [isAutoLogin, setIsAutoLogin] = useState(false)
  const [form] = Form.useForm();
  const onCheckboxChange = (e) => {
    setIsAutoLogin(e.target.checked)
  };

  function login() {
    //return 
    const hide = message.loading("登录中", 0);
    fetchPost(apiRequest.auth.login, {
      body: { username:"admin", password:"Xd8r$3jz" },
    })
      .then((res) => {
        console.log("2222")
          console.log("1111")
          localStorage.setItem("username", res.data.username);
          console.log(123213123)
          history.replace({
            pathname: "/homepage",
            state: {
              data:{
                //...res.data.license_info,
                // service_info:[
                //   ...result
                // ]
              }
            },
          });
          localStorage.setItem("role", "超级管理员");
          fetchGet(apiRequest.userManagement.user, {
            params: {
              username: res.data.username,
            },
            // eslint-disable-next-line max-nested-callbacks
          }).then((res) => {
            localStorage.removeItem("defaultEnvID");
            // eslint-disable-next-line max-nested-callbacks
            handleResponse(res, () => {
              const { username, role } = res.data;
              localStorage.setItem("username", username);
              localStorage.setItem("role", role);
            });
          });
        })
      .catch((e) => {
        console.log(e);
        message.error(e.message);
      })
      .finally(() => hide());
  }

  return (
    <OmpContentWrapper
      wrapperStyle={{ width: "100%", height: "calc(100% - 40px)" }}
    >
      <div className={styles.loginWrapper}>
        <div className={styles.loginContent}>
          <header className={styles.loginTitle}>
            <img className={styles.loginLogo} src={img} />
            <span className={styles.loginOMP}>
              OMP<span className={styles.loginOpenText}>open source</span>
            </span>
          </header>
          <p className={styles.loginInputTitle}>用户名密码登录</p>
          <div
            style={{
              position: "relative",
              top: -20,
              backgroundColor: "#fbe3e2",
              padding: "10px",
              height: "40px",
              color: "#86292e",
              display: "flex",
              justifyContent: "space-between",
              cursor: "pointer",
            }}
            className={
              msgShow ? styles.loginMessageShow : styles.loginMessageHide
            }
            onClick={() => setMsgShow(false)}
          >
            用户名或密码错误
            <CloseCircleFilled
              style={{ color: "#fff", fontSize: 20, marginLeft: "auto" }}
            />
          </div>
          <main
            className={styles.loginInputWrapper}
            style={{ position: "relative", top: msgShow ? 0 : -24 }}
          >
            <Form form={form} onFinish={(e)=>{
              console.log(e)
            }}>
              <Form.Item
                label=""
                name="username"
                key="username"
                rules={[
                  {
                    required: true,
                    message: "请输入用户名",
                  },
                ]}
              >
                <Input
                  prefix={
                    <UserOutlined
                      style={{ color: "#b8b8b8", paddingRight: 10 }}
                    />
                  }
                  style={{ paddingLeft: 10, width: 360, height: 40 }}
                  placeholder="用户名"
                />
              </Form.Item>
              <Form.Item
                label=""
                name="password"
                key="password"
                rules={[
                  {
                    required: true,
                    message: "请输入密码",
                  },
                ]}
              >
                <Input.Password
                  prefix={
                    <LockOutlined
                      style={{ color: "#b8b8b8", paddingRight: 10 }}
                    />
                  }
                  style={{
                    paddingLeft: 10,
                    width: 360,
                    height: 40,
                    marginTop: 10,
                  }}
                  placeholder="请输入密码"
                />
              </Form.Item>
              <div className={styles.loginAuto}>
                <Checkbox checked={isAutoLogin} onChange={onCheckboxChange}>
                  <span style={{ color: "#3a3542" }}>7天自动登录</span>
                </Checkbox>
              </div>
              <Form.Item>
                <Button
                  style={{
                    width: 360,
                    height: 40,
                    fontSize: 16,
                    marginTop: 24,
                  }}
                  type="primary"
                  onClick={() => {
                    setMsgShow(true);
                    login()
                  }}
                  htmlType="submit"
                >
                  登录
                </Button>{" "}
              </Form.Item>
            </Form>
          </main>
          <p className={styles.loginFooter}>一站式运维管理平台</p>
        </div>
      </div>
    </OmpContentWrapper>
  );
})

export default Login;
