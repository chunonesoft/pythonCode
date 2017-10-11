#coding=utf-8
import matplotlib.pyplot as plt

#数据可视化
year = [1950,1970,1990,2010]

pop = [2.3,3.4,5.8,6.5]
#折线图
#plt.plot(year,pop)
plt.fill_between(year,pop,0,color='green')
#
# #轴的标签
plt.xlabel('Year')
plt.ylabel('Population')
#
#轴的标题
plt.title('World Population')
plt.yticks([0,2,4,6,8,10],['0B','2B','4B','6B','8B','10B'])
#
#
 #散点图
#plt.scatter(year,pop)
#
 #直方图
#values = [0,1,2,3,4,1,2,3,4,4,5,2,4,1]
#plt.hist(values,bins=10)


plt.show()