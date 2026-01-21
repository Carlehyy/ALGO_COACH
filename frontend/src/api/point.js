/**
 * 积分相关API请求
 */

import request from './request'

/**
 * 获取积分余额
 */
export function getBalance() {
  return request({
    url: '/points/balance',
    method: 'get'
  })
}

/**
 * 获取积分流水
 */
export function getPointLogs(params) {
  return request({
    url: '/points/logs',
    method: 'get',
    params
  })
}

/**
 * 获取套餐列表
 */
export function getPackages() {
  return request({
    url: '/points/packages',
    method: 'get'
  })
}

/**
 * 创建充值订单
 */
export function createOrder(packageId) {
  return request({
    url: '/points/orders',
    method: 'post',
    data: { package_id: packageId }
  })
}

/**
 * 支付订单（模拟）
 */
export function payOrder(orderNo) {
  return request({
    url: `/points/orders/${orderNo}/callback`,
    method: 'post'
  })
}

/**
 * 查询订单
 */
export function getOrder(orderNo) {
  return request({
    url: `/points/orders/${orderNo}`,
    method: 'get'
  })
}
