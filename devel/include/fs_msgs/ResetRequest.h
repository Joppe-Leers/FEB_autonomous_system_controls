// Generated by gencpp from file fs_msgs/ResetRequest.msg
// DO NOT EDIT!


#ifndef FS_MSGS_MESSAGE_RESETREQUEST_H
#define FS_MSGS_MESSAGE_RESETREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace fs_msgs
{
template <class ContainerAllocator>
struct ResetRequest_
{
  typedef ResetRequest_<ContainerAllocator> Type;

  ResetRequest_()
    : waitOnLastTask(false)  {
    }
  ResetRequest_(const ContainerAllocator& _alloc)
    : waitOnLastTask(false)  {
  (void)_alloc;
    }



   typedef uint8_t _waitOnLastTask_type;
  _waitOnLastTask_type waitOnLastTask;





  typedef boost::shared_ptr< ::fs_msgs::ResetRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::fs_msgs::ResetRequest_<ContainerAllocator> const> ConstPtr;

}; // struct ResetRequest_

typedef ::fs_msgs::ResetRequest_<std::allocator<void> > ResetRequest;

typedef boost::shared_ptr< ::fs_msgs::ResetRequest > ResetRequestPtr;
typedef boost::shared_ptr< ::fs_msgs::ResetRequest const> ResetRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::fs_msgs::ResetRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::fs_msgs::ResetRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::fs_msgs::ResetRequest_<ContainerAllocator1> & lhs, const ::fs_msgs::ResetRequest_<ContainerAllocator2> & rhs)
{
  return lhs.waitOnLastTask == rhs.waitOnLastTask;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::fs_msgs::ResetRequest_<ContainerAllocator1> & lhs, const ::fs_msgs::ResetRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace fs_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::fs_msgs::ResetRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::fs_msgs::ResetRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::fs_msgs::ResetRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::fs_msgs::ResetRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::fs_msgs::ResetRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::fs_msgs::ResetRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::fs_msgs::ResetRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "79b3eea4e90fd67af16afc9085f08e12";
  }

  static const char* value(const ::fs_msgs::ResetRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x79b3eea4e90fd67aULL;
  static const uint64_t static_value2 = 0xf16afc9085f08e12ULL;
};

template<class ContainerAllocator>
struct DataType< ::fs_msgs::ResetRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fs_msgs/ResetRequest";
  }

  static const char* value(const ::fs_msgs::ResetRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::fs_msgs::ResetRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bool waitOnLastTask \n"
;
  }

  static const char* value(const ::fs_msgs::ResetRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::fs_msgs::ResetRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.waitOnLastTask);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct ResetRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::fs_msgs::ResetRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::fs_msgs::ResetRequest_<ContainerAllocator>& v)
  {
    s << indent << "waitOnLastTask: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.waitOnLastTask);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FS_MSGS_MESSAGE_RESETREQUEST_H
